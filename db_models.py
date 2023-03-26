from enum import unique
from flask_sqlalchemy import SQLAlchemy

 
db = SQLAlchemy()


user_favorite_books = db.Table('user_favorite_books',
                                  db.Column('id', db.Integer, autoincrement=True, primary_key=True),
                                  db.Column('user_id', db.Integer,
                                            db.ForeignKey('users.id')),
                                  db.Column('book_id', db.Integer,
                                            db.ForeignKey('books.id')),
                                  db.Column('created_at', db.DateTime(
                                      timezone=True), server_default=db.func.now())
                                  )


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True,comment="page unique identifier")

    public_id = db.Column(db.String(50), unique=True)

    name = db.Column(db.String())

    email = db.Column(db.String, nullable=False, comment="user email")

    hashed_password = db.Column(db.String(), nullable=False,
                              comment="hash of the user password, can not be null ")

    own_books = db.relationship("Book", backref="owner")

    favorite_books = db.relationship("Book", secondary=user_favorite_books)

    def __init__(self, public_id, name, email, hashed_password):
        self.public_id = public_id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True,comment="page unique identifier")

    name = db.Column(db.String(50), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    book_price = db.Column(db.Integer)

    def __init__(self, name, book_price, user_id):
        self.name = name
        self.book_price = book_price
        self.user_id = user_id


