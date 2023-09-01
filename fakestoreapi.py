import requests
import pprint


def fetch_product_data(product_id):
    url = f'https://fakestoreapi.com/products/{product_id}'
    response = requests.get(url)

    if response.status_code == 200:
        product_data = response.json()
        pp = pprint.PrettyPrinter(indent=4, sort_dicts=False)
        pp.pprint(response.json())

        product_name = product_data['title']
        product_price = product_data['price']
        product_description = product_data['description']
        product_category = product_data['category']
        product_rating = product_data['rating']['rate']
        product_count = product_data['rating']['count']

        print('\nProduct name:', product_name)
        print('Product price:', product_price)
        print('Product description', product_description)
        print('Product category:', product_category)
        print('Product rating:', product_rating)
        print('Product count:', product_count)
    else:
        print('Fetching Error. Status code:', response.status_code)


fetch_product_data(int(input('Enter product_id: ')))


