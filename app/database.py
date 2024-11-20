import datetime

import uuid

from sqlalchemy import func

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()



class User(db.Model, UserMixin):
    __tablename__ = 'user_list'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    type_user = db.Column(db.String(20), nullable=False)

    purchase = db.relationship('Purchase', back_populates='user')

    @classmethod
    def password_encryption(cls, password) -> str:
        hash = generate_password_hash(password)
        return hash
    
    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter(cls.name == username).first()

        if user and check_password_hash(user.password, password):
            return user

    @classmethod
    def get_user_by_id(cls, id):
        user = User.query.filter(cls.id == id).first()
        return user

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    last_names = db.Column(db.String(50), nullable=False)
    names = db.Column(db.String(50), nullable=False)
    birth = db.Column(db.Date, nullable=False)

    book = db.relationship("Book", back_populates="author")

    @classmethod
    def full_name(cls, names):
        author = cls.query.filter(cls.names == names).first()
        return f'{author.names}, {author.last_names}'

class Book(db.Model):
    __tablename__ = 'book'
    isbn = db.Column(db.String(12), primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship("Author", back_populates="book")

    purchase = db.relationship("Purchase")

    @classmethod
    def books_sold(cls):
        units = db.session.query(Purchase.book_id, cls.title, cls.price, func.count(Purchase.book_id).label('units_sold')).join(cls, Purchase.book_id == cls.isbn).all()#.group_by(Purchase.book_id, cls.title,cls.price).order_by(func.count(Purchase.book_id).desc(), cls.title.asc())
        return units


class Purchase(db.Model):
    __tablename__ = 'purchase'
    uuid = db.Column(db.String(36), primary_key=True, nullable=False, unique=True)
    purchased_at = db.Column(db.DateTime, default= datetime.datetime.now())

    book_id = db.Column(db.String(12), db.ForeignKey('book.isbn'))
    book = db.relationship('Book', back_populates="purchase")

    user_id = db.Column(db.Integer, db.ForeignKey('user_list.id'))
    user = db.relationship("User", back_populates="purchase")

    @classmethod
    def users_purchase(cls, user):
        user_books = db.session.query(cls.purchased_at, Book.isbn, Book.title).join(cls, cls.book_id == Book.isbn).filter(cls.user_id == user.id).all()
        return user_books