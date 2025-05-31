import tkinter as tk
from tkinter import ttk
from models import SessionLocal, Book
import pandas as pd
from tabulate import tabulate


class BookViewerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Books Database Viewer")
        self.root.geometry("1200x800")

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create search frame
        self.search_frame = ttk.LabelFrame(
            self.main_frame, text="Search", padding="5")
        self.search_frame.grid(
            row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            self.search_frame, textvariable=self.search_var, width=40)
        self.search_entry.grid(row=0, column=0, padx=5)

        # Search button
        self.search_button = ttk.Button(
            self.search_frame, text="Search", command=self.search_books)
        self.search_button.grid(row=0, column=1, padx=5)

        # Category filter
        self.category_var = tk.StringVar(value="All Categories")
        self.categories = self.get_categories()
        self.category_combo = ttk.Combobox(self.search_frame, textvariable=self.category_var,
                                           values=["All Categories"] + self.categories, state="readonly")
        self.category_combo.grid(row=0, column=2, padx=5)
        self.category_combo.bind(
            '<<ComboboxSelected>>', lambda e: self.filter_by_category())

        # Create treeview
        self.tree = ttk.Treeview(self.main_frame, columns=("Title", "Price", "Category", "Rating", "In Stock", "Availability"),
                                 show="headings", height=20)

        # Configure columns
        self.tree.heading("Title", text="Title")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Rating", text="Rating")
        self.tree.heading("In Stock", text="In Stock")
        self.tree.heading("Availability", text="Availability")

        # Set column widths
        self.tree.column("Title", width=400)
        self.tree.column("Price", width=100)
        self.tree.column("Category", width=150)
        self.tree.column("Rating", width=100)
        self.tree.column("In Stock", width=100)
        self.tree.column("Availability", width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid layout
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))

        # Stats frame
        self.stats_frame = ttk.LabelFrame(
            self.main_frame, text="Statistics", padding="5")
        self.stats_frame.grid(row=2, column=0, columnspan=2,
                              sticky=(tk.W, tk.E), pady=5)

        # Stats labels
        self.total_books_label = ttk.Label(
            self.stats_frame, text="Total Books: 0")
        self.total_books_label.grid(row=0, column=0, padx=10)

        self.avg_price_label = ttk.Label(
            self.stats_frame, text="Average Price: £0.00")
        self.avg_price_label.grid(row=0, column=1, padx=10)

        self.categories_label = ttk.Label(
            self.stats_frame, text="Categories: 0")
        self.categories_label.grid(row=0, column=2, padx=10)

        # Load initial data
        self.load_books()
        self.update_stats()

    def get_categories(self):
        """Get list of categories from database."""
        db = SessionLocal()
        try:
            categories = db.query(Book.category).distinct().all()
            return [cat[0] for cat in categories]
        finally:
            db.close()

    def load_books(self, search_term=None, category=None):
        """Load books from database into treeview."""
        db = SessionLocal()
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Build query
            query = db.query(Book)
            if search_term:
                query = query.filter(Book.title.ilike(f"%{search_term}%"))
            if category and category != "All Categories":
                query = query.filter(Book.category == category)

            # Get books
            books = query.all()

            # Insert into treeview
            for book in books:
                self.tree.insert("", tk.END, values=(
                    book.title,
                    f"£{book.price:.2f}",
                    book.category,
                    book.rating,
                    "Yes" if book.in_stock else "No",
                    book.availability
                ))
        finally:
            db.close()

    def search_books(self):
        """Search books by title."""
        search_term = self.search_var.get()
        category = self.category_var.get()
        self.load_books(search_term, category)
        self.update_stats()

    def filter_by_category(self):
        """Filter books by category."""
        category = self.category_var.get()
        search_term = self.search_var.get()
        self.load_books(search_term, category)
        self.update_stats()

    def update_stats(self):
        """Update statistics display."""
        db = SessionLocal()
        try:
            total_books = db.query(Book).count()
            avg_price = db.query(Book.price).all()
            avg_price = sum(price[0] for price in avg_price) / \
                len(avg_price) if avg_price else 0
            categories = db.query(Book.category).distinct().count()

            self.total_books_label.config(text=f"Total Books: {total_books}")
            self.avg_price_label.config(
                text=f"Average Price: £{avg_price:.2f}")
            self.categories_label.config(text=f"Categories: {categories}")
        finally:
            db.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookViewerGUI(root)
    root.mainloop()
