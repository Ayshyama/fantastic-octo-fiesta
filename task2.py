import json
import requests
import sqlite3
from random import randint
from datetime import datetime, timedelta


def fetch_product_data(product_id):
    response = requests.get(f'https://fakestoreapi.com/products/{product_id}')
    if response.status_code == 200:
        if response.text:  # Check if the response is not empty
            try:
                product_data = response.json()
                return product_data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for product ID {product_id}: {e}")
        else:
            print(f"Empty response for product ID {product_id}.")
    else:
        print(f"Failed to fetch data for product ID {product_id}. Status code: {response.status_code}")


def generate_random_datetime():
    return datetime.now() - timedelta(seconds=randint(0, 365 * 24 * 3600))


def create_products_table(cursor):
    cursor.executescript("""DROP TABLE IF EXISTS "products"; 
    CREATE TABLE IF NOT EXISTS 'products' (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "title" TEXT,
    "category" TEXT,
    "price" REAL,
    "description" TEXT,
    "date_added" TEXT
);
""")


def insert_product_into_db(cursor, product_data):
    cursor.execute('''INSERT INTO "products" ("title", "category", "price", "description", "date_added")
    VALUES (?, ?, ?, ?, ?);''',
                   (product_data["title"], product_data["category"], product_data["price"], product_data["description"],
                    generate_random_datetime()))


if __name__ == '__main__':
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()
    create_products_table(cur)
    a, b = int(input('Enter start id: ')), int(input('Enter end id: '))
    for i in range(a, b+1):
        product_data = fetch_product_data(i)
        if product_data:
            insert_product_into_db(cur, product_data)
    conn.commit()
    cur.execute('SELECT * FROM "products";')
    print(*cur.fetchall(), sep='\n')
    conn.close()






