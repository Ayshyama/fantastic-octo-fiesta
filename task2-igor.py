import requests
import sqlite3
from datetime import datetime, timedelta
import random
import json


def fetch_product_data(product_id):
    url = f"https://fakestoreapi.com/products/{product_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            product_data = response.json()
            return product_data
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response for product ID {product_id}: {e}")
            return None
    else:
        print(f"Failed to fetch data for product ID {product_id}. Status code: {response.status_code}")
        return None



def create_products_table(cursor):
    cursor.executescript('''
    DROP TABLE IF EXISTS "products"; 
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        title TEXT,
        category TEXT,
        price REAL,
        description TEXT,
        date_added DATETIME,
        total_cost REAL
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


if __name__ == "__main__":
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    create_products_table(cursor)

    start_id = int(input("Enter the starting product ID: "))
    end_id = int(input("Enter the ending product ID: "))



    for product_id in range(start_id, end_id + 1):
        product_data = fetch_product_data(product_id)
        if product_data:
            insert_product_into_db(cursor, product_data)

    conn.commit()
    conn.close()
