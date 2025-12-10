"""
Work.ua Job Scraper

Скрипт збирає вакансії з сайту Work.ua.
Збирає: назву вакансії, компанію, локацію, зарплату, короткий опис та посилання на оголошення.
Результат зберігається у файлі work_ua.json у форматі JSON.
"""

import requests
from bs4 import BeautifulSoup
import json


def normalize_text(text: str) -> str:
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
    text = ' '.join(text.split())

    return text


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

data = []

for page in range(1, 11):
    print(f'Парсимо сторінку: {page} ...')

    url = f'https://www.work.ua/jobs/?page={page}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    cards = soup.find_all(
        'div',
        class_='card card-hover card-visited wordwrap job-link js-hot-block mt-sm sm:mt-lg'
    )

    for item in cards:
        h2_tag = item.find('h2', class_='my-0')
        name_work = h2_tag.get_text(strip=True) if h2_tag else "Без назви"

        logo_tag = item.find('img', class_='preview-img preview-img-logo')
        company = logo_tag.get('alt') if logo_tag else "Без компанії"

        spans = item.find('div', class_='mt-xs').find_all('span', class_='')
        location = None
        for sp in spans:
            if sp.find('span', class_='strong-600'):
                continue
            txt = sp.get_text(strip=True)
            if not txt or 'км' in txt:
                continue
            txt = txt.replace(',', '').strip()
            if txt:
                location = normalize_text(txt)
                break

        salary = "Зарплата не вказана"
        strong_tags = item.find_all('span', class_='strong-600')
        for st in strong_tags:
            t = st.get_text(strip=True)
            if 'грн' in t:
                salary = normalize_text(t)
                break

        desc_tag = item.find(
            'p',
            class_='ellipsis ellipsis-line ellipsis-line-3 text-default-7 mb-0'
        )
        short_description = normalize_text(desc_tag.get_text(strip=True)) if desc_tag else ""

        link = h2_tag.find('a')['href'] if h2_tag and h2_tag.find('a') else "#"
        link_on_work = 'https://www.work.ua' + link

        data.append({
            'name_work': normalize_text(name_work),
            'company': normalize_text(company),
            'location': normalize_text(location) if location else None,
            'salary': salary,
            'short_description': short_description,
            'link_on_work': link_on_work
        })

with open('work_ua.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Парсинг завершено, дані записано у work_ua.json")
