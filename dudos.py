import json
import requests


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


for i in range(10000):
    for j in range(20):
        print(fetch_product_data(j))
