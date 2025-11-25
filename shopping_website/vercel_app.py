import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, Product, Order, OrderItem
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'shopping_secret_key_dev')

# Database configuration for Vercel Postgres
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_URL', 'sqlite:///shopping.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

def init_sample_data():
    """Add sample products if database is empty"""
    if Product.query.count() == 0:
        sample_products = [
            Product(name="Web Development Basics", description="Learn HTML, CSS and JavaScript fundamentals", 
                   cost_price=5.00, sell_price=19.99, category="ebooks"),
            Product(name="Python Programming Guide", description="Complete Python programming tutorial", 
                   cost_price=8.00, sell_price=24.99, category="ebooks"),
            Product(name="Database Design Manual", description="Learn SQL and database principles", 
                   cost_price=6.00, sell_price=22.99, category="ebooks"),
            
            Product(name="Flask Web Development Course", description="Build web applications with Flask", 
                   cost_price=20.00, sell_price=49.99, category="courses"),
            Product(name="JavaScript Masterclass", description="Advanced JavaScript programming", 
                   cost_price=15.00, sell_price=39.99, category="courses"),
            Product(name="Responsive Design Workshop", description="Create mobile-friendly websites", 
                   cost_price=12.00, sell_price=34.99, category="courses"),
            
            Product(name="Code Editor Pro", description="Professional code editing software", 
                   cost_price=10.00, sell_price=29.99, category="software"),
            Product(name="Web Design Toolkit", description="Complete web design software package", 
                   cost_price=15.00, sell_price=44.99, category="software"),
            Product(name="Database Manager", description="Manage your databases efficiently", 
                   cost_price=18.00, sell_price=54.99, category="software"),
            Product(name="Project Planning App", description="Organize your development projects", 
                   cost_price=8.00, sell_price=24.99, category="software")
        ]
        
        for product in sample_products:
            db.session.add(product)
        db.session.commit()

@app.route('/')
def index():
    # Get products by category (like restaurant menu categories)
    products = {
        'ebooks': Product.query.filter_by(category='ebooks').all(),
        'courses': Product.query.filter_by(category='courses').all(),
        'software': Product.query.filter_by(category='software').all()
    }
    return render_template('index.html', products=products)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/api/products')
def api_products():
    """API endpoint for JavaScript to get product data"""
    products = Product.query.all()
    products_dict = {}
    for product in products:
        category = product.category
        if category not in products_dict:
            products_dict[category] = []
        products_dict[category].append(product.to_dict())
    
    return jsonify(products_dict)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Get customer details
        email = request.form.get('email')
        phone = request.form.get('phone')
        suburb = request.form.get('suburb')
        cart_data = request.form.get('cart_data')  # JSON string from JavaScript
        
        # Basic validation
        if not email or not phone or not suburb:
            flash('All fields are required')
            return redirect(url_for('checkout'))
        
        if not cart_data:
            flash('Your cart is empty')
            return redirect(url_for('cart'))
        
        try:
            import json
            cart_items = json.loads(cart_data)
            
            if not cart_items:
                flash('Your cart is empty')
                return redirect(url_for('cart'))
            
            # Calculate total
            total = 0
            for item in cart_items:
                total += float(item['price']) * int(item['quantity'])
            
            # Create order (like restaurant system)
            order = Order(
                customer_email=email,
                customer_phone=phone,
                customer_suburb=suburb,
                total_amount=total
            )
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Add order items
            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=int(item['id']),
                    product_name=item['name'],
                    quantity=int(item['quantity']),
                    price_at_purchase=float(item['price'])
                )
                db.session.add(order_item)
            
            db.session.commit()
            
            return redirect(url_for('confirmation', order_id=order.id))
            
        except Exception as e:
            db.session.rollback()
            flash('Error processing order. Please try again.')
            return redirect(url_for('checkout'))
    
    return render_template('checkout.html')

@app.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('confirmation.html', order=order)

@app.route('/admin')
def admin():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    
    # Calculate profit data for admin
    total_revenue = 0
    total_cost = 0
    
    for order in orders:
        total_revenue += order.total_amount
        for item in order.order_items:
            if item.product:
                total_cost += item.product.cost_price * item.quantity
    
    profit_data = {
        'total_revenue': total_revenue,
        'total_cost': total_cost,
        'total_profit': total_revenue - total_cost
    }
    
    return render_template('admin.html', orders=orders, profit_data=profit_data)

# Create tables and add sample data
@app.before_first_request
def create_tables():
    db.create_all()
    init_sample_data()

if __name__ == '__main__':
    # For local development
    with app.app_context():
        db.create_all()
        init_sample_data()
    app.run(debug=True)
