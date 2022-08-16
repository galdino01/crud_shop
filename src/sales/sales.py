from pymongo import MongoClient
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

import os
import uuid

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/rpc')

MONGO_SERVER = os.environ['MONGO_SERVER']
SALES_PORT = int(os.environ['SALES_PORT'])

def get_sales_database():
    client = MongoClient(MONGO_SERVER)
    return client.sales

def get_products_database():
    client = MongoClient(MONGO_SERVER)
    return client.products

def get_customers_database():
    client = MongoClient(MONGO_SERVER)
    return client.customers

def create_sale(customer_id, product_id, amount):
    sales_db = get_sales_database()
    products_db = get_products_database()
    customers_db = get_customers_database()

    customer_name = customers_db.customers.find_one({'_id': customer_id})['name']

    product_name = products_db.products.find_one({'_id': product_id})['name']
    product_price = products_db.products.find_one({'_id': product_id})['price']
    product_amount = products_db.products.find_one({'_id': product_id})['quantity']

    update_stock = int(product_amount) - int(amount)

    products_db.products.update_one({'_id': product_id}, {'$set': {'quantity': str(update_stock)}})

    formatted_price = product_price.replace('.', '')
    formatted_price = formatted_price.replace(',', '.')
    profit = int(amount) * (float(formatted_price) - (float(formatted_price) - (float(formatted_price) * 0.10)))
    profit = format(profit, '.2f')
    formatted_price = ((float(formatted_price) * 0.10) + float(formatted_price)) * int(amount)
    formatted_price = format(formatted_price, '.2f')

    unt_price = product_price.replace('.', '')
    unt_price = unt_price.replace(',', '.')
    unt_price = format(float(unt_price), '.2f')

    sale = sales_db.sales.insert_one({
        '_id': str(uuid.uuid4()),
        'customer': customer_name,
        'product': product_name,
        'unt_price': unt_price,
        'amount': amount,
        'profit': profit,
        'price': formatted_price,
    })

    return f"Sale {sale.inserted_id} created."

def get_sales():
    sales = list()
    db = get_sales_database()

    for sale in db.sales.find():
        sales.append(sale)

    return sales

def count_sales():
    sales = list()
    db = get_sales_database()

    for sale in db.sales.find():
        sales.append(sale)

    return len(sales)

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('0.0.0.0', SALES_PORT))

    server.register_function(create_sale, 'create_sale')
    server.register_function(get_sales, 'get_sales')
    server.register_function(count_sales, 'count_sales')

    server.register_introspection_functions()
    server.serve_forever()