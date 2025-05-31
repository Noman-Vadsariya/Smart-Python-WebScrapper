import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration for SQLite
DB_CONFIG = {
    'sqlite_path': os.getenv('SQLITE_PATH', 'sqlite:///books_demo.db')
}

# Scraping configuration
BASE_URL = 'https://books.toscrape.com'
CATALOGUE_URL = f'{BASE_URL}/catalogue'

# Export configuration
EXPORT_DIR = 'exports'
CSV_DIR = os.path.join(EXPORT_DIR, 'csv')
EXCEL_DIR = os.path.join(EXPORT_DIR, 'excel')

# Create export directories if they don't exist
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(EXCEL_DIR, exist_ok=True)
