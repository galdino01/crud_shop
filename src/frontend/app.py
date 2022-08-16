from flask import Flask
from flask import render_template
from flask import request   

import xmlrpc.client
import os

PRODUCTS_URL = os.environ['PRODUCTS_URL']
CUSTOMERS_URL = os.environ['CUSTOMERS_URL']
SALES_URL = os.environ['SALES_URL']

app = Flask(__name__)

@app.route("/home", methods=['GET', 'POST'])
def index():
    products = xmlrpc.client.ServerProxy(PRODUCTS_URL)
    customers = xmlrpc.client.ServerProxy(CUSTOMERS_URL)
    sales = xmlrpc.client.ServerProxy(SALES_URL)

    count_type_products = products.count_type_products()
    count_products = products.count_products()
    count_customers = customers.count_customers()
    count_sales = sales.count_sales()

    return render_template('index.html', sizeof_products=count_products, sizeof_type_products=count_type_products, sizeof_customers=count_customers, sizeof_sales=count_sales)

@app.route("/products", methods=['GET', 'POST'])
def products():
    client = xmlrpc.client.ServerProxy(PRODUCTS_URL)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = request.form['quantity']
        price = request.form['price']

        client.create_product(name, description, quantity, price)

    products = client.get_products()

    return render_template('products/index.html', products=products)

@app.route("/customers", methods=['GET', 'POST'])
def customers():
    client = xmlrpc.client.ServerProxy(CUSTOMERS_URL)

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']

        client.create_customer(name, phone)

    customers = client.get_customers()

    return render_template('customers/index.html', customers=customers)

@app.route("/sales", methods=['GET', 'POST'])
def sales():
    products = xmlrpc.client.ServerProxy(PRODUCTS_URL)
    customers = xmlrpc.client.ServerProxy(CUSTOMERS_URL)
    sales = xmlrpc.client.ServerProxy(SALES_URL)

    products_list = products.get_products()
    customers_list = customers.get_customers()

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        product_id = request.form['product_id']
        amount = request.form['amount']

        sales.create_sale(customer_id, product_id, amount)

    sales_list = sales.get_sales()

    return render_template('sales/index.html', sales=sales_list, products=products_list, customers=customers_list)