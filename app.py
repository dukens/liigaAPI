from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from faker import Faker
import random

# Generate sample data.
fake = Faker()

# Setup Flask and sqlalchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Setup Models, Order of things
# 1. start easy --> add primary keys
# 2. Add "obvious columns" --> name and price.
#   2.1 Add constraints. Cant be empty, must be unique
# 3. Keep adding fields. Customer fields

# 4. Create a relationship with the columns. customer_id to refer to Customer.
#   - 'Order has a customer'


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(500),nullable=False)
    city = db.Column(db.String(50),nullable=False)
    postcode = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),nullable=False, unique=True)

    # Create a pseudo-column to Order table. Makes 
    #   - Order.Customer returns customer object
    #   - Customer.orders returns orders related to a customer

    # customer has many orders
    # order has one customer
    orders = db.relationship('Order', backref='customer')

# Many to many relationship
# - order has many products
# - product has many orders

order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    shipped_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    coupon_code = db.Column(db.String(50))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    products = db.relationship('Product', secondary=order_product)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)



# Create fake data
def add_customers():
    for _ in range(100):
        customer = Customer(
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            address = fake.street_address(),
            city = fake.city(),
            postcode = fake.postcode(),
            email = fake.email()
        )
        db.session.add(customer)
    db.session.commit()

def add_orders():
    customers = Customer.query.all()

    for _ in range(1000):
        #choose a random customer
        customer = random.choice(customers)

        ordered_date = fake.date_time_this_year()
        shipped_date = random.choices([None, fake.date_time_between(start_date=ordered_date)], [10, 90])[0]

        delivered_date = None
        if shipped_date:
            delivered_date = random.choices([None, fake.date_time_between(start_date=shipped_date)],[50,50])[0]
        
        coupon_code = random.choices([None, '50OFF', 'FREESHIPPING', 'BUYONEGETONE'], [80,5,5,5])[0]

        order = Order(
            customer_id=customer.id,
            order_date=ordered_date,
            shipped_date=shipped_date,
            delivered_date=delivered_date,
            coupon_code=coupon_code
        )

        db.session.add(order)
    
    db.session.commit()

def add_products():
    for _ in range(10):
        product = Product(
            name=fake.color_name(),
            price=random.randint(10,100)
        )
        db.session.add(product)
    db.session.commit()

def add_order_products():
    orders = Order.query.all()
    products = Product.query.all()

    for order in orders:
        k = random.randint(1,3)

        purchased_products = random.sample(products, k)
        order.products.extend(purchased_products)

    db.session.commit()

def create_random_data():
    db.create_all()
    add_customers()
    add_orders()
    add_products()
    add_order_products()