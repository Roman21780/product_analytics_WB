# parser.py
import requests
from bs4 import BeautifulSoup
from .models import Product


def parse_wildberries(query):
    url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for item in soup.select('.product-card'):
        name = item.select_one('.product-card__name').text.strip()
        price = float(item.select_one('.price__lower-price').text.replace('₽', '').replace(' ', '').strip())
        sale_price = float(item.select_one('.price__lower-price').text.replace('₽', '').replace(' ',
                                                                                                '').strip())  # Пример, может отличаться
        rating = float(item.select_one('.product-card__rating').text.strip()) if item.select_one(
            '.product-card__rating') else 0.0
        reviews = int(
            item.select_one('.product-card__count').text.strip().replace('отзывов', '').strip()) if item.select_one(
            '.product-card__count') else 0

        Product.objects.create(
            name=name,
            price=price,
            sale_price=sale_price,
            rating=rating,
            review_count=reviews
        )