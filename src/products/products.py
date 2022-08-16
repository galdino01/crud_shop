from pymongo import MongoClient
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

import os
import uuid

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/rpc')

MONGO_SERVER = os.environ['MONGO_SERVER']
PRODUCTS_PORT = int(os.environ['PRODUCTS_PORT'])

def get_database():
    client = MongoClient(MONGO_SERVER)
    return client.products

def create_product(name, description, quantity, price):
    db = get_database()

    product = db.products.insert_one({
        '_id': str(uuid.uuid4()),
        'name': name,
        'description': description,
        'quantity': quantity,
        'price': price
    })

    return f"Product {product.inserted_id} created."

def get_products():
    products = list()
    db = get_database()

    for product in db.products.find():
        products.append(product)

    return products

def count_type_products():
    products = list()
    db = get_database()

    for product in db.products.find():
        products.append(product)

    return len(products)

def count_products():
    db = get_database()

    stock = 0
    for product in db.products.find():
        stock += int(product['quantity'])

    return stock

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('0.0.0.0', PRODUCTS_PORT))

    server.register_function(create_product, 'create_product')
    server.register_function(get_products, 'get_products')
    server.register_function(count_type_products, 'count_type_products')
    server.register_function(count_products, 'count_products')

    server.register_introspection_functions()
    server.serve_forever()