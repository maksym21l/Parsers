"""
Auto.ria Car Scraper

Цей скрипт збирає дані про вживані автомобілі з сайту Auto.ria.
Збирає: марку та модель, рік, ціну, пробіг, місто та посилання на оголошення.
Зберігає результат у autoria.json.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}


data = []

# Кількість сторінок, які парсимо
pages = 4

for page in range(1, pages + 1):
    print(f"Парсимо сторінку {page}...")

    url = f'https://auto.ria.com/uk/car/used/?page={page}'
    req = requests.get(url, headers=headers)

    if req.status_code != 200:
        print(f"Помилка завантаження сторінки {page}")
        continue

    soup = BeautifulSoup(req.text, 'lxml')
    cars = soup.find_all('div', class_='content-bar')

    for car in cars:
        try:
            title_block = car.find('div', class_='item ticket-title')
            marka_model = title_block.find('a').text.strip()

            # рік зазвичай стоїть останнім словом у заголовку
            year = title_block.text.strip().split()[-1]

            # ціна
            priceUSD = car.find('div', class_='price-ticket')['data-main-price'] + ' $'

            mileage = car.find('li', class_='item-char js-race').text.strip()
            city = car.find('li', class_='item-char view-location js-location').text.strip()

            link = car.find('a', class_='m-link-ticket').get('href')

            data.append({
                "marka_model": marka_model,
                "year": year,
                "priceUSD": priceUSD,
                "mileage": mileage,
                "city": city,
                "link": link
            })

        except:
            # Якщо щось не знайдено — просто пропускаємо
            continue

    time.sleep(random.randint(1, 2))

# запис у файл
with open('autoria.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print('Готово! Дані збережено у autoria.json')
