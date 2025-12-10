"""
Work.ua Job Scraper

Скрипт збирає вакансії з сайту Work.ua.
Збирає: назву вакансії, компанію, локацію, зарплату, короткий опис та посилання.
Зберігає результат у work_ua.json.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random


def normalize_text(text):
    """Очищує текст від зайвих пробілів і спецсимволів"""
    if not text:
        return text

    replacements = {
        '\u00A0': ' ',
        '\u202F': ' ',
        '\u2009': ' ',
        '\u2007': ' ',
        '\u2060': ' ',
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)

    text = text.replace('–', '-').replace('—', '-')
    return ' '.join(text.split())


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
    print(f'Парсимо сторінку {page} ...')
    url = f'https://www.work.ua/jobs/?page={page}'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Помилка завантаження сторінки {page}")
        continue

    soup = BeautifulSoup(response.text, 'lxml')
    cards = soup.find_all(
        'div',
        class_='card card-hover card-visited wordwrap job-link js-hot-block mt-sm sm:mt-lg'
    )

    for item in cards:
        try:
            # Назва вакансії
            h2_tag = item.find('h2', class_='my-0')
            name_work = h2_tag.get_text(strip=True) if h2_tag else "Без назви"

            # Компанія
            logo_tag = item.find('img', class_='preview-img preview-img-logo')
            company = logo_tag.get('alt') if logo_tag else "Без компанії"

            # Локація
            location = None
            spans = item.find('div', class_='mt-xs').find_all('span', class_='')
            for sp in spans:
                if sp.find('span', class_='strong-600'):
                    continue
                txt = sp.get_text(strip=True)
                if txt and 'км' not in txt:
                    location = normalize_text(txt)
                    break

            # Зарплата
            salary = "Зарплата не вказана"
            for st in item.find_all('span', class_='strong-600'):
                t = st.get_text(strip=True)
                if 'грн' in t:
                    salary = normalize_text(t)
                    break

            # Короткий опис
            desc_tag = item.find('p', class_='ellipsis ellipsis-line ellipsis-line-3 text-default-7 mb-0')
            short_description = normalize_text(desc_tag.get_text(strip=True)) if desc_tag else ""

            # Посилання
            link = h2_tag.find('a')['href'] if h2_tag and h2_tag.find('a') else "#"
            link_on_work = 'https://www.work.ua' + link

            # Додаємо до списку
            data.append({
                'name_work': normalize_text(name_work),
                'company': normalize_text(company),
                'location': normalize_text(location) if location else None,
                'salary': salary,
                'short_description': short_description,
                'link_on_work': link_on_work
            })
        except:
            continue

    # Пауза, щоб сервер не блокував
    time.sleep(random.randint(1, 2))

# Збереження результатів
with open('work_ua.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Готово! Дані записано у work_ua.json")
