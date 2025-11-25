from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json
import os
from datetime import datetime
from models import db, Product, Order, OrderItem

app = Flask(__name__, instance_path='/tmp')
app.secret_key = 'shopping_secret_key'

# Database configuration - try multiple environment variable names
database_url = (
    os.environ.get('POSTGRES_URL') or 
    os.environ.get('DATABASE_URL') or
    os.environ.get('POSTGRES_PRISMA_URL')
)

if database_url:
    # Fix postgres:// to postgresql:// if needed
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Local development - use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Initialize database
db.init_app(app)

def seed_products():
    """Load and insert products from JSON file"""
    try:
        with open('products.json', 'r') as f:
            products_data = json.load(f)
        
        for category, products in products_data.items():
            for product_data in products:
                product = Product(
                    id=product_data['id'],
                    name=product_data['name'],
                    description=product_data.get('description', ''),
                    cost_price=product_data['cost_price'],
                    sell_price=product_data['sell_price'],
                    category=product_data['category'],
                    image_url=product_data.get('image_url')  # Support optional image URLs
                )
                db.session.add(product)
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding products: {e}")
        return False

# Don't call initialize_database() at module level - it won't work in Vercel's serverless environment

@app.route('/init')
def init_db():
    """Manual database initialization endpoint"""
    try:
        # Check for any Postgres environment variable
        db_url = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')
        if not db_url:
            # Return diagnostic info
            return jsonify({
                'error': 'No database configured',
                'env_vars': {
                    'POSTGRES_URL': 'set' if os.environ.get('POSTGRES_URL') else 'not set',
                    'DATABASE_URL': 'set' if os.environ.get('DATABASE_URL') else 'not set',
                    'app_db_uri': app.config.get('SQLALCHEMY_DATABASE_URI', 'not set')[:50]
                }
            }), 500
        
        # Create all tables
        db.create_all()
        
        # Check if products already exist
        existing_count = Product.query.count()
        if existing_count > 0:
            return jsonify({
                'status': 'already_initialized',
                'product_count': existing_count
            })
        
        # Load products from JSON file
        with open('products.json', 'r') as f:
            products_data = json.load(f)
        
        # Add all products to database
        for category, products in products_data.items():
            for product_data in products:
                product = Product(
                    id=product_data['id'],
                    name=product_data['name'],
                    description=product_data.get('description', ''),
                    cost_price=product_data['cost_price'],
                    sell_price=product_data['sell_price'],
                    category=product_data['category']
                )
                db.session.add(product)
        
        db.session.commit()
        product_count = Product.query.count()
        
        return jsonify({
            'status': 'success',
            'message': f'Database initialized with {product_count} products'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Display all products organized by category"""
    try:
        # Auto-initialize database if empty (first request)
        try:
            if Product.query.count() == 0:
                db.create_all()
                seed_products()
        except:
            # Tables don't exist yet
            db.create_all()
            seed_products()
        
        # Get all products from database
        all_products = Product.query.all()
        
        # Organize products by category
        products = {
            'ebooks': [],
            'courses': [],
            'software': []
        }
        
        for product in all_products:
            if product.category in products:
                products[product.category].append(product.to_dict())
        
        return render_template('index.html', products=products)
    except Exception as e:
        print(f"Error loading products: {e}")
        flash('Error loading products')
        return render_template('index.html', products={'ebooks': [], 'courses': [], 'software': []})

@app.route('/cart')
def cart():
    """Display shopping cart"""
    return render_template('cart.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Handle checkout process"""
    if request.method == 'POST':
        try:
            # Get customer details
            email = request.form.get('email')
            phone = request.form.get('phone')
            suburb = request.form.get('suburb')
            cart_data = request.form.get('cart_data')
            
            # Validate input
            if not all([email, phone, suburb, cart_data]):
                flash('All fields are required')
                return redirect(url_for('checkout'))
            
            # Parse cart data
            cart_items = json.loads(cart_data)
            
            if not cart_items:
                flash('Your cart is empty')
                return redirect(url_for('cart'))
            
            # Calculate total
            total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
            
            # Create order
            order = Order(
                customer_email=email,
                customer_phone=phone,
                customer_suburb=suburb,
                total_amount=total_amount,
                status='completed'
            )
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Create order items
            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['id'],
                    product_name=item['name'],
                    quantity=item['quantity'],
                    price_at_purchase=item['price']
                )
                db.session.add(order_item)
            
            db.session.commit()
            
            # Store order ID in session for confirmation page
            session['last_order_id'] = order.id
            session['last_order_total'] = total_amount
            
            flash('Order placed successfully!')
            return redirect(url_for('confirmation'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error processing order: {e}")
            flash('Error processing your order. Please try again.')
            return redirect(url_for('checkout'))
    
    return render_template('vercel_checkout.html')

@app.route('/confirmation')
def confirmation():
    """Display order confirmation"""
    order_id = session.get('last_order_id')
    order_total = session.get('last_order_total', 0)
    
    return render_template('confirmation.html', order_id=order_id, order_total=order_total)

@app.route('/admin')
def admin():
    """Display admin dashboard with all orders"""
    try:
        # Get all orders with their items
        orders = Order.query.order_by(Order.order_date.desc()).all()
        orders_data = [order.to_dict() for order in orders]
        
        return render_template('admin.html', orders=orders_data)
    except Exception as e:
        print(f"Error loading orders: {e}")
        flash('Error loading orders')
        return render_template('admin.html', orders=[])

@app.route('/api/products')
def api_products():
    """API endpoint to get all products"""
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>')
def api_order(order_id):
    """API endpoint to get specific order details"""
    try:
        order = Order.query.get_or_404(order_id)
        return jsonify(order.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Health check endpoint for Vercel
@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'database': 'connected'})

if __name__ == '__main__':
    app.run(debug=True)
