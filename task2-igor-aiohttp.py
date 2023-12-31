import requests
import sqlite3
from datetime import datetime, timedelta
import random
import json
import aiohttp
import asyncio


def fetch_product_data(product_id):
    url = f"https://fakestoreapi.com/products/{product_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            product_data = response.json()
            return product_data
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response for {product_id}: {e}")
            return None
    else:
        print(f"Failed to fetch data for {product_id}. Status code: {response.status_code}")
        return None


async def fetch_product_data_async(product_id, session):
    url = f"https://fakestoreapi.com/products/{product_id}"
    async with session.get(url) as response:
        if response.status == 200:
            try:
                product_data = await response.json()
                return product_data
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON response for product ID {product_id}: {e}")
        else:
            print(f"Failed to fetch data for product ID {product_id}. Status code: {response.status}")


def create_products_table(cursor):
    cursor.executescript('''
    DROP TABLE IF EXISTS "products"; 
    CREATE TABLE IF NOT EXISTS "products" (
        "id" INTEGER PRIMARY KEY,
        "title" TEXT,
        "category" TEXT,
        "price" REAL,
        "description" TEXT,
        "date_added" DATETIME,
        "total_cost" REAL
    )''')
    print("products.db and table 'products' created successfully")


def insert_product_into_db(cursor, product_data):
    title = product_data["title"]
    category = product_data["category"]
    price = product_data["price"]
    description = product_data["description"]
    date_added = datetime.now() - timedelta(days=random.randint(1, 365))
    total_cost = price * random.randint(1, 10)

    cursor.execute(
        '''INSERT INTO "products" ("title", "category", "price", "description", "date_added", "total_cost") VALUES (?, ?, ?, ?, ?, ?)''',
        (title, category, price, description, date_added, total_cost))
    print(f"Inserted product '{title}' into the database.")


async def main():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    create_products_table(cursor)

    start_id = int(input("Enter the starting product ID: "))
    end_id = int(input("Enter the ending product ID: "))

    async with aiohttp.ClientSession() as session:
        tasks = []
        for product_id in range(start_id, end_id + 1):
            tasks.append(fetch_product_data_async(product_id, session))

        product_data_list = await asyncio.gather(*tasks)

        for product_data in product_data_list:
            if product_data:
                insert_product_into_db(cursor, product_data)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    asyncio.run(main())
