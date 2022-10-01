from web_app import db
from datetime import datetime


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(255))
    # mail = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    year = db.Column(db.Integer, default=20)
    # department = db.Column(db.String(255))
    menu = db.Column(db.String(100))
    count = db.Column(db.String(100))
    order_time = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)