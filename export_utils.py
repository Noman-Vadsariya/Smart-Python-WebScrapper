import pandas as pd
from datetime import datetime
from models import SessionLocal, Book
from config import CSV_DIR, EXCEL_DIR
import logging

logger = logging.getLogger(__name__)


def export_to_csv():
    """Export all books to a CSV file."""
    try:
        db = SessionLocal()
        books = db.query(Book).all()

        # Convert to DataFrame
        data = []
        for book in books:
            data.append({
                'Title': book.title,
                'Price': book.price,
                'Availability': book.availability,
                'Rating': book.rating,
                'Category': book.category,
                'Description': book.description,
                'UPC': book.upc,
                'Product Type': book.product_type,
                'Price (excl. tax)': book.price_excl_tax,
                'Price (incl. tax)': book.price_incl_tax,
                'Tax': book.tax,
                'Number of Reviews': book.num_reviews,
                'In Stock': book.in_stock,
                'Last Updated': book.updated_at
            })

        df = pd.DataFrame(data)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'books_export_{timestamp}.csv'
        filepath = f'{CSV_DIR}/{filename}'

        # Export to CSV
        df.to_csv(filepath, index=False)
        logger.info(f"Successfully exported {len(books)} books to {filepath}")

    except Exception as e:
        logger.error(f"Error exporting to CSV: {str(e)}")
    finally:
        db.close()


def export_to_excel():
    """Export all books to an Excel file."""
    try:
        db = SessionLocal()
        books = db.query(Book).all()

        # Convert to DataFrame
        data = []
        for book in books:
            data.append({
                'Title': book.title,
                'Price': book.price,
                'Availability': book.availability,
                'Rating': book.rating,
                'Category': book.category,
                'Description': book.description,
                'UPC': book.upc,
                'Product Type': book.product_type,
                'Price (excl. tax)': book.price_excl_tax,
                'Price (incl. tax)': book.price_incl_tax,
                'Tax': book.tax,
                'Number of Reviews': book.num_reviews,
                'In Stock': book.in_stock,
                'Last Updated': book.updated_at
            })

        df = pd.DataFrame(data)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'books_export_{timestamp}.xlsx'
        filepath = f'{EXCEL_DIR}/{filename}'

        # Export to Excel
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Books')

            # Auto-adjust columns' width
            worksheet = writer.sheets['Books']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[chr(
                    65 + idx)].width = max_length + 2

        logger.info(f"Successfully exported {len(books)} books to {filepath}")

    except Exception as e:
        logger.error(f"Error exporting to Excel: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    # Example usage
    export_to_csv()
    export_to_excel()
