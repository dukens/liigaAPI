from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Setup Flask and sqlalchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Setup Models, Order of things
# 1. start easy --> add primary keys
# 2. Add "obvious columns" --> name and price.
#   2.1 Add constraints. Cant be empty, must be unique
# 3. Keep adding fields. Customer fields


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(500),nullable=False)
    city = db.Column(db.String(50),nullable=False)
    postcode = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),nullable=False, unique=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    shipped_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    coupon_code = db.Column(db.String(50))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)

#