"""
SvitBudov Apartment Scraper (Simple Clean Version)

Скрипт збирає дані про квартири зі SvitBudov.
Збирає: ціну, кімнати, площу, поверх, адресу, опис та посилання.
Зберігає у apartment.json
"""

import json
import time
import random
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()

all_apartment_list = []

# Кількість сторінок, які парсимо
pages = 4

for page in range(1, pages + 1):
    print(f"Парсимо сторінку {page}...")

    url = f"https://svitbudov.com/prodazh-kvartyry/?page={page}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "lxml")

    apartments = soup.find_all("div", class_="ticket")

    for apartment in apartments:
        # Основні параметри
        price_tag = apartment.find("span", class_="price")
        if price_tag:
            price = price_tag.text.strip()
        else:
            price = "Not found"

        # Наступні значення йдуть по черзі
        room_tag = price_tag.find_next("span") if price_tag else None
        area_tag = room_tag.find_next("span") if room_tag else None
        floor_tag = area_tag.find_next("span") if area_tag else None

        count_room = room_tag.text.strip() if room_tag else "Not found"
        area = area_tag.text.strip() if area_tag else "Not found"
        floor = floor_tag.text.strip() if floor_tag else "Not found"

        # Адреса
        address_tag = apartment.find("a", class_="ticket__address")
        if not address_tag:
            address_tag = apartment.find("a", class_="ticket__title")

        if address_tag:
            address = address_tag.text.strip()
            link = "https://svitbudov.com" + address_tag.get("href")
        else:
            address = "Not found"
            link = "Not found"

        # Опис
        description_tag = apartment.find("label", class_="ticket__description")
        if description_tag:
            description = " ".join(description_tag.get_text().split())
            description = description[:150] + "..."
        else:
            description = "Not found"

        # Збираємо у список
        all_apartment_list.append({
            "price": price,
            "count_room": count_room,
            "area": area,
            "floor": floor,
            "address": address,
            "description": description,
            "link": link
        })

    # Пауза, щоб не спамити сервер
    time.sleep(random.randint(2, 4))

# Збереження
with open("apartment.json", "w", encoding="utf-8") as file:
    json.dump(all_apartment_list, file, indent=4, ensure_ascii=False)

print("Готово! Дані збережені в apartment.json")
