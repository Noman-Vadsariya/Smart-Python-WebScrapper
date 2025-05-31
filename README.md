# Books to Scrape - Web Scraper

A Python-based web scraper that extracts product data from the Books to Scrape website (https://books.toscrape.com/). The scraper collects detailed book information and stores it in a PostgreSQL database, with support for exporting data to CSV and Excel formats.

## Features

- Scrapes book information including title, price, availability, rating, category, and more
- Stores data in PostgreSQL database
- Exports data to CSV and Excel formats
- Handles pagination and multiple categories
- Implements rate limiting to be respectful to the server
- Includes error handling and logging

## Prerequisites

- Python 3.x
- PostgreSQL database
- Virtual environment (recommended)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your database configuration:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=book_scraper
DB_USER=your_username
DB_PASSWORD=your_password
```

5. Create the PostgreSQL database:

```bash
createdb book_scraper
```

## Usage

1. Initialize the database:

```python
from models import init_db
init_db()
```

2. Run the scraper:

```bash
python scraper.py
```

3. Export data to CSV or Excel:

```bash
python export_utils.py
```

## Project Structure

- `scraper.py`: Main scraper module
- `models.py`: Database models and configuration
- `config.py`: Configuration settings
- `export_utils.py`: Data export utilities
- `requirements.txt`: Project dependencies

## Data Export

The scraper supports exporting data in two formats:

1. CSV Export:

   - Files are saved in the `exports/csv` directory
   - Filenames include timestamps for versioning

2. Excel Export:
   - Files are saved in the `exports/excel` directory
   - Includes auto-adjusted column widths
   - Filenames include timestamps for versioning

## Error Handling

The scraper includes comprehensive error handling:

- Logs errors to console
- Continues scraping even if individual books fail
- Maintains database transaction integrity
- Handles network errors gracefully

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
