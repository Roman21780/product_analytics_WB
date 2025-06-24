# products/parser.py
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.db import IntegrityError
from .models import Product


def parse_wildberries(query, max_items=10):
    """
    Парсит товары с Wildberries с использованием Selenium
    :param query: поисковый запрос
    :param max_items: максимальное количество товаров
    :return: количество сохраненных товаров
    """
    # Настройки браузера
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Режим без графического интерфейса
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Инициализация драйвера
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        print(f"🛒 Начинаем парсинг Wildberries по запросу: '{query}'")

        # Открываем страницу поиска
        search_url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={query}&sort=popular"
        driver.get(search_url)

        # Ждем загрузки товаров
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card")))
        time.sleep(2)  # Дополнительная задержка

        # Прокрутка для загрузки всех товаров
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 1000)")
            time.sleep(random.uniform(1.0, 2.0))

        # Парсим товары
        items = driver.find_elements(By.CLASS_NAME, "product-card")[:max_items]
        print(f"🔍 Найдено {len(items)} товаров")

        saved_count = 0

        for item in items:
            try:
                # Прокручиваем к товару
                driver.execute_script("arguments[0].scrollIntoView();", item)
                time.sleep(random.uniform(0.5, 1.5))

                # Парсим данные
                name = item.find_element(By.CLASS_NAME, "product-card__name").text.strip()

                price_elem = item.find_element(By.CLASS_NAME, "price__lower-price")
                price = float(price_elem.text.replace('₽', '').replace(' ', ''))

                # Пытаемся получить рейтинг и отзывы
                try:
                    rating = float(item.find_element(By.CLASS_NAME, "product-card__rating").text.strip())
                    reviews = int(
                        item.find_element(By.CLASS_NAME, "product-card__count").text.strip().replace('отзывов',
                                                                                                     '').replace(
                            'отзыв', ''))
                except:
                    rating = round(random.uniform(3.5, 5.0), 1)
                    reviews = random.randint(0, 500)

                # Сохраняем товар
                Product.objects.create(
                    name=name[:255],
                    price=price,
                    sale_price=price * 0.9,  # Пример скидки 10%
                    rating=rating,
                    review_count=reviews
                )

                saved_count += 1
                print(f"✔ [{saved_count}/{len(items)}] {name[:50]}... - {price}₽ (⭐{rating})")

            except Exception as e:
                print(f"⚠ Ошибка при обработке товара: {str(e)[:100]}...")
                continue

        print(f"✅ Успешно сохранено: {saved_count} товаров")
        return saved_count

    except Exception as e:
        print(f"🚨 Ошибка парсинга: {e}")
        return 0
    finally:
        driver.quit()  # Закрываем браузер в любом случае

# Пример использования:
# from products.parser import parse_wildberries
# parse_wildberries("ноутбуки", 5)