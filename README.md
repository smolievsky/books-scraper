# Books to Scrape - Web Scraper 🕷️📚

A script to scrape book information from the website [Books to Scrape](https://books.toscrape.com/).

## 📌 functionality

Scrapes the following data for each book:
Title
Category
Rating
Price (Excluding and Including Tax)
Tax
Availability
UPC (Universal Product Code)
Saves the collected data into a CSV file books_full_info.csv

## requierments
- Python
- requests
- BeautifulSoup
- pandas

## how to use

```bash
pip install -r requirements.txt
python books_scraper.py
