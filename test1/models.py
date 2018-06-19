
from exts import db

class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    bookname = db.Column(db.String(100),nullable = False)
    bookprice = db.Column(db.Float,nullable =False)
    book_num = db.Column(db.Integer)
class Clothes(db.Model):
    __tablename__ = 'clothes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clothesname = db.Column(db.String(100),nullable = False)
    clotheprice = db.Column(db.Float, nullable=False)
    clothes_num = db.Column(db.Integer)

class Digital(db.Model):
    __tablename__ = 'digital'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    digitalname = db.Column(db.String(100),nullable = False)
    digitalprice = db.Column(db.Float, nullable=False)
    digital_num = db.Column(db.Integer)

class Eating(db.Model):
    __tablename__ = 'eating'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eatingname = db.Column(db.String(100), nullable=False)
    eatingprice = db.Column(db.Float, nullable=False)
    eating_num = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    money = db.Column(db.Float, default=0.00)
