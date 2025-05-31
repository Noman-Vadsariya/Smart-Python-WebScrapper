import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Optional
from models import Book, SessionLocal
from config import BASE_URL, CATALOGUE_URL, CSV_DIR
import logging
import re
import os
import csv
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BATCH_SIZE = 20
CSV_FILENAME = os.path.join(
    CSV_DIR, f'books_live_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
CSV_HEADERS = [
    'title', 'price', 'availability', 'rating', 'category', 'description', 'upc',
    'product_type', 'price_excl_tax', 'price_incl_tax', 'tax', 'num_reviews', 'in_stock'
]


def write_books_to_csv(books: List[Dict], file_path: str, write_header: bool = False):
    """Append a batch of books to the CSV file."""
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        if write_header:
            writer.writeheader()
        for book in books:
            writer.writerow(book)


class BookScraper:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.csv_initialized = False

    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage."""
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None

    def clean_price(self, price_str: str) -> float:
        """Clean price string and convert to float."""
        try:
            # Remove any special characters and convert to float
            cleaned_price = re.sub(r'[^\d.]', '', price_str)
            return float(cleaned_price)
        except (ValueError, TypeError):
            logger.error(f"Error cleaning price: {price_str}")
            return 0.0

    def get_book_details(self, book_url: str) -> Optional[Dict]:
        """Extract detailed information from a book's page."""
        soup = self.get_page(book_url)
        if not soup:
            return None

        try:
            # Extract book information
            product_info = {}
            table = soup.find('table', class_='table-striped')
            if table:
                for row in table.find_all('tr'):
                    header = row.find('th').text.strip()
                    value = row.find('td').text.strip()
                    product_info[header] = value

            # Extract other details
            title = soup.find('h1').text.strip()
            price_text = soup.find('p', class_='price_color').text.strip()
            price = self.clean_price(price_text)

            availability_text = soup.find(
                'p', class_='availability').text.strip()
            availability = int(re.search(r'\d+', availability_text).group()
                               if re.search(r'\d+', availability_text) else '0')

            rating = soup.find('p', class_='star-rating')['class'][1]
            description = soup.find('div', id='product_description')
            description = description.find_next(
                'p').text.strip() if description else ''
            category = soup.find('ul', class_='breadcrumb').find_all('li')[
                2].text.strip()

            return {
                'title': title,
                'price': price,
                'availability': availability,
                'rating': rating,
                'category': category,
                'description': description,
                'upc': product_info.get('UPC', ''),
                'product_type': product_info.get('Product Type', ''),
                'price_excl_tax': self.clean_price(product_info.get('Price (excl. tax)', '0')),
                'price_incl_tax': self.clean_price(product_info.get('Price (incl. tax)', '0')),
                'tax': self.clean_price(product_info.get('Tax', '0')),
                'num_reviews': int(product_info.get('Number of reviews', '0')),
                'in_stock': availability > 0
            }
        except Exception as e:
            logger.error(
                f"Error parsing book details from {book_url}: {str(e)}")
            return None

    def get_category_books(self, category_url: str):
        books_batch = []
        page_num = 1
        db = SessionLocal()
        try:
            while True:
                url = f"{category_url}/page-{page_num}.html" if page_num > 1 else category_url
                soup = self.get_page(url)
                if not soup:
                    break
                book_links = soup.find_all('h3')
                if not book_links:
                    break
                for book in book_links:
                    book_url = f"{BASE_URL}/catalogue/{book.find('a')['href'].replace('../', '')}"
                    book_details = self.get_book_details(book_url)
                    if book_details:
                        books_batch.append(book_details)
                    if len(books_batch) >= BATCH_SIZE:
                        # Write to CSV
                        write_books_to_csv(
                            books_batch, CSV_FILENAME, write_header=not self.csv_initialized)
                        self.csv_initialized = True
                        # Write to DB
                        for book_data in books_batch:
                            try:
                                db.merge(Book(**book_data))
                            except Exception as e:
                                logger.error(
                                    f"DB error for book {book_data.get('title')}: {e}")
                        db.commit()
                        books_batch.clear()
                    time.sleep(1)
                next_button = soup.find('li', class_='next')
                if not next_button:
                    break
                page_num += 1
                time.sleep(1)
            # Write any remaining books
            if books_batch:
                write_books_to_csv(books_batch, CSV_FILENAME,
                                   write_header=not self.csv_initialized)
                self.csv_initialized = True
                for book_data in books_batch:
                    try:
                        db.merge(Book(**book_data))
                    except Exception as e:
                        logger.error(
                            f"DB error for book {book_data.get('title')}: {e}")
                db.commit()
        finally:
            db.close()

    def scrape_all_books(self):
        soup = self.get_page(BASE_URL)
        if not soup:
            return
        categories = soup.find('div', class_='side_categories').find_all('a')
        # Skip the first 'Books' category (it's a superset)
        for category in categories[1:]:
            category_url = f"{BASE_URL}/{category['href']}"
            logger.info(f"Scraping category: {category.text.strip()}")
            self.get_category_books(category_url)
            time.sleep(2)


def main():
    scraper = BookScraper()
    scraper.scrape_all_books()


if __name__ == "__main__":
    main()
