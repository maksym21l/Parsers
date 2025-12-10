"""
Auto.ria Car Scraper

Цей скрипт збирає дані про вживані автомобілі з сайту Auto.ria.
Збирає: марку та модель, рік випуску, ціну, пробіг, місто та посилання на оголошення.
Результат зберігається у файлі autoria.json у форматі JSON.
"""

import requests
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, як Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

data = []

for i in range(1, 6):
    print(f'Парсимо сторінку {i} ...')
    url = f'https://auto.ria.com/uk/car/used/?page={i}'
    req = requests.get(url, headers=headers)

    if req.status_code != 200:
        print(f"Не вдалося завантажити сторінку {i}")
        continue

    soup = BeautifulSoup(req.text, 'lxml')
    block = soup.find_all('div', class_='content-bar')

    for item in block:
        try:
            marka_model = item.find('div', class_='item ticket-title').find('a').text
            year = item.find('div', class_='item ticket-title').text.strip().split(' ')[-1]
            priceUSD = item.find('div', class_='price-ticket')['data-main-price'] + ' $'
            mileage = item.find('li', class_='item-char js-race').text.strip()
            city = item.find('li', class_='item-char view-location js-location').text.strip()
            link = item.find('a', class_='m-link-ticket').get('href')

            data.append({
                'marka_model': marka_model,
                'year': year,
                'priceUSD': priceUSD,
                'mileage': mileage,
                'city': city,
                'link': link
            })
        except AttributeError:
            continue

with open('autoria.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print('Парсинг завершено, дані збережено у файлі autoria.json')
