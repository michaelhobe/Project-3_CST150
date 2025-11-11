from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'shopping_secret_key'

# Data files (like restaurant system)
PRODUCTS_FILE = 'products.json'
ORDERS_FILE = 'orders.json'

# Initialize data (adapted from restaurant initialize_data function)
def initialize_data():
    try:
        with open(PRODUCTS_FILE, 'r') as f:
            products = json.load(f)
    except:
        # Default products if file doesn't exist
        products = {
            'ebooks': [
                {'id': 1, 'name': 'Web Dev Basics', 'cost_price': 5.00, 'sell_price': 19.99, 'category': 'ebooks'},
                {'id': 2, 'name': 'Python Guide', 'cost_price': 8.00, 'sell_price': 24.99, 'category': 'ebooks'}
            ],
            'courses': [
                {'id': 3, 'name': 'Flask Course', 'cost_price': 20.00, 'sell_price': 49.99, 'category': 'courses'},
                {'id': 4, 'name': 'JavaScript Basics', 'cost_price': 15.00, 'sell_price': 39.99, 'category': 'courses'}
            ]
        }
        with open(PRODUCTS_FILE, 'w') as f:
            json.dump(products, f)
    
    try:
        with open(ORDERS_FILE, 'r') as f:
            orders = json.load(f)
    except:
        orders = []
        with open(ORDERS_FILE, 'w') as f:
            json.dump(orders, f)
    
    return products, orders

# Save data (from restaurant system)
def save_data(data_type, data):
    if data_type == 'products':
        with open(PRODUCTS_FILE, 'w') as f:
            json.dump(data, f)
    elif data_type == 'orders':
        with open(ORDERS_FILE, 'w') as f:
            json.dump(data, f)

# Load initial data
products, orders = initialize_data()

# Routes (adapted from restaurant system)
@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Get customer details (like restaurant table_number)
        email = request.form.get('email')
        phone = request.form.get('phone')
        suburb = request.form.get('suburb')
        
        # Basic validation
        if not email or not phone or not suburb:
            flash('All fields are required')
            return redirect(url_for('checkout'))
        
        # For now, just redirect to confirmation
        return redirect(url_for('confirmation'))
    
    return render_template('checkout.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)