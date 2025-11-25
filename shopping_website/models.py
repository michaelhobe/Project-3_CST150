# models.py - Database models for Vercel Postgres

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    cost_price = db.Column(db.Float, nullable=False)
    sell_price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'cost_price': self.cost_price,
            'sell_price': self.sell_price,
            'category': self.category
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_email = db.Column(db.String(255), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_suburb = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')
    
    # Relationship to order items
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'customer_suburb': self.customer_suburb,
            'total_amount': self.total_amount,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'status': self.status,
            'items': [item.to_dict() for item in self.order_items]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)  # Store name at purchase time
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)
    
    # Relationship to product
    product = db.relationship('Product', backref='order_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'price_at_purchase': self.price_at_purchase,
            'subtotal': self.quantity * self.price_at_purchase
        }
