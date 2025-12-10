"""
SvitBudov Apartment Scraper

Скрипт збирає дані про квартири на продаж з сайту SvitBudov.com.
Збирає: ціну, кількість кімнат, площу, поверх, адресу, короткий опис та посилання на оголошення.
Результат зберігається у файлі apartment.json у форматі JSON.
"""

import random
import time
import json
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()

all_apartment_list = []

for i in range(1, 5):
    print(f'Парсимо сторінку: {i} ...')

    url = f'https://svitbudov.com/prodazh-kvartyry/?page={i}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    req = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(req.text, 'lxml')

    apartments = soup.find_all('div', class_='ticket')

    for apartment in apartments:
        price = apartment.find('span', class_='price').text
        count_room = apartment.find('span', class_='price').find_next('span').text
        area = apartment.find('span', class_='price').find_next('span').find_next('span').text
        floor = apartment.find('span', class_='price').find_next('span').find_next('span').find_next('span').text

        address_tag = apartment.find('a', class_='ticket__address')
        if address_tag:
            address = address_tag.text.strip()
            link = 'https://svitbudov.com' + address_tag.get('href')
        else:
            title_tag = apartment.find('a', class_='ticket__title')
            if title_tag:
                address = title_tag.text.strip()
                link = 'https://svitbudov.com' + title_tag.get('href')
            else:
                address = 'Not found'
                link = 'Not found'

        description_tag = apartment.find('label', class_='ticket__description')
        if description_tag:
            description = ' '.join(description_tag.get_text().split())[:150] + '...'
        else:
            description = 'Not found'

        all_apartment_list.append({
            'price': price,
            'count_room': count_room,
            'area': area,
            'floor': floor,
            'address': address,
            'description': description,
            'link': link
        })

    time.sleep(random.randint(2, 4))

with open('apartment.json', 'w', encoding='utf-8') as file:
    json.dump(all_apartment_list, file, indent=4, ensure_ascii=False)

print('Парсинг завершено, дані збережено у файлі apartment.json')
