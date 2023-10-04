import json
import requests

import aiohttp
import asyncio

import sqlite3
from datetime import datetime, timedelta
import random


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
    print("SQLite database 'products.db' and table 'products' created successfully.")


def insert_product_into_db(cursor, product_data):
    title = product_data["title"]
    category = product_data["category"]
    price = product_data["price"]
    description = product_data["description"]
    date_added = datetime.now() - timedelta(days=random.randint(1, 365))
    total_cost = price * random.randint(1, 10)

    cursor.execute(
        "INSERT INTO products (title, category, price, description, date_added, total_cost) VALUES (?, ?, ?, ?, ?, ?)",
        (title, category, price, description, date_added, total_cost))
    print(f"Inserted product '{title}' into the database.")


async def fetch_product_data_async(session, product_id):
    url = f"https://fakestoreapi.com/products/{product_id}"
    async with session.get(url) as response:
        if response.status == 200:
            try:
                product_data = await response.json()
                return product_data
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON response for product ID {product_id}: {e}")
                return None
        else:
            print(f"Failed to fetch data for product ID {product_id}. Status code: {response.status}")
            return None


# Define a list of 5 different product IDs
product_ids = [1, 2, 3, 4, 5]


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []

        # Create tasks for each product ID and send 100 concurrent requests for each
        for product_id in product_ids:
            tasks.extend([fetch_product_data_async(session, product_id) for _ in range(5)])

        results = await asyncio.gather(*tasks)

        # Create or connect to the SQLite database
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        # Create products table
        create_products_table(cursor)

        # Fetch and insert product data into the database
        for product_data in results:
            if product_data:
                insert_product_into_db(cursor, product_data)

        # Commit changes and close the database connection
        conn.commit()
        conn.close()


if __name__ == "__main__":
    # Run the asynchronous fetch and insert process
    asyncio.run(main())
