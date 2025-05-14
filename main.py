import os
import requests
from bs4 import BeautifulSoup, FeatureNotFound
import fake_useragent
import pandas as pd
import time

def get_headers():
    user = fake_useragent.FakeUserAgent().random
    return {"user-agent": user}

def get_response(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Ошибка загрузки страницы:{url}. Ошибка{e}")
        return None
    
def get_soup(response):
    try:
        soup = BeautifulSoup(response.text, "lxml")
        return soup
    except FeatureNotFound:
        print(f" Парсер 'lxml не установлен")
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    
def get_book_info(soup):

    ul_block = soup.find("ul", class_="breadcrumb")
    table_block = soup.find("table", class_="table table-striped")
    return {
        "title": ul_block.find("li", class_="active").text,
        "category": ul_block.select("li:not(.active) > a")[-1].text,
        "rating": soup.find("p", class_="star-rating").attrs["class"][1],
        "UPC": table_block.find_all("td")[0].text,
        "Price(excl.tax)": table_block.find_all("td")[2].text[2:],
        "Price(Incl.tax)": table_block.find_all("td")[3].text[2:],
        "Tax": table_block.find_all("td")[4].text[2:],
        "Availability": table_block.find_all("td")[5].text
    }


def main():
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    headers = get_headers()
    books_data = []

    for page in range(1, 51):
        url = base_url.format(page)
        print(f"Обрабатываю страницу:{page}")

        response = get_response(url=url, headers=headers)
        if not response:
            continue

        soup = get_soup(response=response)
        books = soup.find_all("div", class_="image_container")

        for book in books:
            book_path = book.find("a")["href"]
            book_url = "https://books.toscrape.com/catalogue/" + book_path

            book_response = get_response(book_url, headers=headers)

            book_soup = get_soup(book_response)
            book_info = get_book_info(book_soup)

            books_data.append(book_info)
            time.sleep(0.5)
        
        time.sleep(1)
    
    df = pd.DataFrame(books_data)
    df["rating"] = df["rating"].map({"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5})
    df["Availability"] = df["Availability"].str.extract(r'(\d+)')

    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, "books_full_info.csv")
    df.to_csv(save_path, index=False, encoding="utf-8")
    print("Сбор данных завершён. Результат сохранён в books_full_info.csv")

if __name__ == "__main__":
    main()