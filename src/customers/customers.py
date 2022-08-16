from pymongo import MongoClient
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

import os
import uuid

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/rpc')

MONGO_SERVER = os.environ['MONGO_SERVER']
CUSTOMERS_PORT = int(os.environ['CUSTOMERS_PORT'])

def get_database():
    client = MongoClient(MONGO_SERVER)
    return client.customers

def create_customer(name, phone):
    db = get_database()

    customer = db.customers.insert_one({
        '_id': str(uuid.uuid4()),
        'name': name,
        'phone': phone
    })

    return f'Customer {customer.inserted_id} created.'

def get_customers():
    customers = list()
    db = get_database()

    for customer in db.customers.find():
        customers.append(customer)

    return customers

def count_customers():
    customers = list()
    db = get_database()

    for customer in db.customers.find():
        customers.append(customer)

    return len(customers)

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('0.0.0.0', CUSTOMERS_PORT))

    server.register_function(create_customer, 'create_customer')
    server.register_function(get_customers, 'get_customers')
    server.register_function(count_customers, 'count_customers')

    server.register_introspection_functions()
    server.serve_forever()