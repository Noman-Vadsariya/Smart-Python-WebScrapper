from models import SessionLocal, Book
import pandas as pd
from tabulate import tabulate


def view_database_stats():
    """Display basic statistics about the database."""
    db = SessionLocal()
    try:
        total_books = db.query(Book).count()
        categories = db.query(Book.category).distinct().all()
        categories = [cat[0] for cat in categories]

        print("\n=== Database Statistics ===")
        print(f"Total books: {total_books}")
        print(f"Number of categories: {len(categories)}")
        print("\nCategories:")
        for cat in categories:
            count = db.query(Book).filter(Book.category == cat).count()
            print(f"- {cat}: {count} books")
    finally:
        db.close()


def view_books(limit=10, category=None):
    """Display books from the database."""
    db = SessionLocal()
    try:
        query = db.query(Book)
        if category:
            query = query.filter(Book.category == category)

        books = query.limit(limit).all()

        # Convert to list of dicts for display
        books_data = []
        for book in books:
            books_data.append({
                'Title': book.title,
                'Price': f"£{book.price:.2f}",
                'Category': book.category,
                'Rating': book.rating,
                'In Stock': 'Yes' if book.in_stock else 'No',
                'Availability': book.availability
            })

        if books_data:
            print(
                f"\n=== Books in Database (showing {len(books_data)} of {query.count()}) ===")
            print(tabulate(books_data, headers='keys', tablefmt='grid'))
        else:
            print("No books found in the database.")
    finally:
        db.close()


def export_to_pandas():
    """Export database to pandas DataFrame for analysis."""
    db = SessionLocal()
    try:
        books = db.query(Book).all()
        data = []
        for book in books:
            data.append({
                'title': book.title,
                'price': book.price,
                'category': book.category,
                'rating': book.rating,
                'availability': book.availability,
                'in_stock': book.in_stock,
                'num_reviews': book.num_reviews
            })
        return pd.DataFrame(data)
    finally:
        db.close()


if __name__ == "__main__":
    print("=== Books to Scrape Database Viewer ===")

    # Show database statistics
    view_database_stats()

    # Show sample of books
    print("\nSample of books in database:")
    view_books(limit=5)

    # Export to pandas for analysis
    df = export_to_pandas()
    print("\n=== Price Statistics by Category ===")
    print(df.groupby('category')['price'].agg(
        ['count', 'mean', 'min', 'max']).round(2))
