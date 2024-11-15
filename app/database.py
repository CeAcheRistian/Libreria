import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'user_list'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    type_user = db.Column(db.String(20), nullable=False)

    purchase = db.relationship('Purchase', back_populates='user')


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    last_names = db.Column(db.String(50), nullable=False)
    names = db.Column(db.String(50), nullable=False)
    birth = db.Column(db.Date, nullable=False)

    book = db.relationship("Book", back_populates="author")


class Book(db.Model):
    __tablename__ = 'book'
    isbn = db.Column(db.String(12), primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship("Author", back_populates="book")

    purchase = db.relationship("Purchase")


class Purchase(db.Model):
    __tablename__ = 'purchase'
    uuid = db.Column(db.String(36), primary_key=True, nullable=False, unique=True)
    purchased_at = db.Column(db.DateTime, default= datetime.datetime.now())

    book_id = db.Column(db.String(12), db.ForeignKey('book.isbn'))
    book = db.relationship('Book', back_populates="purchase")

    user_id = db.Column(db.Integer, db.ForeignKey('user_list.id'))
    user = db.relationship("User", back_populates="purchase")

