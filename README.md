# Books to Scrape - Python Web Scraper

![Banner](gallery/Screenshot%202025-05-31%20at%2010.50.03%E2%80%AFPM.png)

A powerful, user-friendly Python web scraper for the [Books to Scrape](https://books.toscrape.com/) website. Collects detailed book data, stores it in a database, and provides both command-line and graphical interfaces for browsing, searching, and exporting your data.

---

## 🚀 Features

- Scrapes book information: title, price, availability, rating, category, and more
- Stores data in a database (PostgreSQL or SQLite)
- Exports data to CSV and Excel formats
- Handles pagination and all categories
- Rate limiting and robust error handling
- **NEW:** Browse and search your data with a modern GUI (Tkinter) or CLI viewer

---

## 🖼️ Live Demo

### GUI Viewer

Browse, search, and filter your books with a beautiful desktop app:

![GUI Demo 1](gallery/Screenshot%202025-05-31%20at%2010.50.19%E2%80%AFPM.png)
![GUI Demo 2](gallery/Screenshot%202025-05-31%20at%2010.51.01%E2%80%AFPM.png)

### Data Export Example

Export your data to Excel or CSV for further analysis:

![Excel Export](gallery/Screenshot%202025-05-31%20at%2010.53.15%E2%80%AFPM.png)

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your database:**
   - For PostgreSQL, create a `.env` file:
     ```
     DB_HOST=localhost
     DB_PORT=5432
     DB_NAME=book_scraper
     DB_USER=your_username
     DB_PASSWORD=your_password
     ```
   - For SQLite, default config is used (see `config.py`).

---

## ⚡ Usage

1. **Initialize the database:**
   ```python
   from models import init_db
   init_db()
   ```
2. **Run the scraper:**
   ```bash
   python scraper.py
   ```
3. **Export data to CSV or Excel:**
   ```bash
   python export_utils.py
   ```
4. **View your data:**
   - **Graphical Viewer:**
     ```bash
     python gui_viewer.py
     ```
   - **Command-Line Viewer:**
     ```bash
     python view_data.py
     ```

---

## 📁 Project Structure

- `scraper.py`: Main scraper module
- `models.py`: Database models and configuration
- `config.py`: Configuration settings
- `export_utils.py`: Data export utilities
- `gui_viewer.py`: Tkinter GUI for browsing/searching books
- `view_data.py`: CLI tool for stats and quick views
- `requirements.txt`: Project dependencies
- `gallery/`: Screenshots and demo images

---

## 📤 Data Export

- **CSV:** Saved in `exports/csv/` with timestamps
- **Excel:** Saved in `exports/excel/` with auto-adjusted columns

---

## 🛡️ Error Handling

- Logs errors to console
- Continues scraping even if individual books fail
- Maintains database transaction integrity
- Handles network errors gracefully

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
