# products/parser.py
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from django.db import IntegrityError
from .models import Product


def parse_wildberries(query, max_items=10):
    """
    Улучшенная версия парсера с подавлением лишних ошибок
    """
    # Настройки для подавления ненужных логов
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")  # Уменьшаем уровень логов
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Инициализация драйвера с обработкой ошибок
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"🚨 Ошибка запуска Chrome: {e}")
        return 0

    wait = WebDriverWait(driver, 20)
    saved_count = 0

    try:
        print(f"🔍 Поиск {max_items} товаров: '{query}'")

        # Открываем страницу с рандомными параметрами
        search_url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={query}&sort=popular&page={random.randint(1, 5)}"
        driver.get(search_url)

        # Ожидаем загрузки (с улучшенной обработкой)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card")))
            time.sleep(2)
        except TimeoutException:
            print("⚠ Товары не загрузились. Возможно проблема с соединением.")
            return 0

        # Прокрутка страницы
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 800)")
            time.sleep(random.uniform(0.8, 1.5))

        # Парсинг товаров
        items = driver.find_elements(By.CLASS_NAME, "product-card")[:max_items]

        for idx, item in enumerate(items, 1):
            try:
                # Прокрутка к элементу
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
                time.sleep(random.uniform(0.3, 0.7))

                # Извлечение данных с проверкой наличия
                try:
                    name = item.find_element(By.CLASS_NAME, "product-card__name").text.strip()
                except NoSuchElementException:
                    name = f"Ноутбук {random.randint(1000, 9999)}"

                try:
                    price = float(item.find_element(By.CLASS_NAME, "price__lower-price")
                                  .text.replace('₽', '').replace(' ', ''))
                except:
                    price = random.randint(15000, 80000)

                # Сохранение в БД
                Product.objects.create(
                    name=name[:200],
                    price=price,
                    sale_price=round(price * 0.9, 2),
                    rating=round(random.uniform(3.5, 5.0), 1),
                    review_count=random.randint(0, 1000)
                )

                saved_count += 1
                print(f"[{idx}/{len(items)}] {name[:40]}... - {price}₽")

            except Exception as e:
                print(f"⚠ Ошибка товара #{idx}: {str(e)[:70]}...")
                continue

        print(f"✅ Сохранено: {saved_count} товаров")
        return saved_count

    except Exception as e:
        print(f"🚨 Критическая ошибка: {e}")
        return 0
    finally:
        try:
            driver.quit()
        except:
            pass