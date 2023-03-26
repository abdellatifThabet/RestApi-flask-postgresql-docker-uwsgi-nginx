from flask import Flask, request, Response, jsonify
from flask_restx import Resource, Api, fields
from flask_migrate import Migrate

#from werkzeug.security import generate_password_hash,check_password_hash
## as a hash function we'll be  using argon
from argon2 import PasswordHasher
ph = PasswordHasher()
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import uuid
import jwt
import datetime
import os
from werkzeug.exceptions import NotFound, Forbidden

from db_models import Book, User
from models import UserModel, BookModel
from config_app import config

app = Flask(__name__)
app.config.from_object(config)

 
from db_models import db 
db.init_app(app)
migrate = Migrate(app, db)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-tokens'
    }
}
api = Api(app, authorizations=authorizations)
# blueprint_v1 = Blueprint('api', __name__, url_prefix='/api')
# app.register_blueprint(blueprint_v1)
# api = Api(blueprint_v1, version='1.0', title='kivi cart manager api', ordered=True, validate=True,
#              description='Restful api to manage user cart',
#              authorizations=authorizations
#              )

user_post_model = api.model('user_post_model', {
    'name': fields.String(required=True, description='name of the user', default='user 1'),
    'email': fields.String(required=True, description='email of the user', default='user1@gmail.com'),
    'passwd': fields.String(required=True, description='password of the facebook account', default='54460380'),
})

login_post_model = api.model('login_post_model', {
    'email': fields.String(required=True, description='name of the user'),
    'passwd': fields.String(required=True, description='password of the facebook account', format='password'),
})

book_post_model = api.model('book_post_model', {
    'book_name': fields.String(required=True, description='name of the book'),
    'book_price': fields.Integer(required=True, description='price of the book'),
})


@api.route('/register', doc={'example': 'register'})
class UserManagemet(Resource):
    @api.response(200, 'user added')
    @api.response(400, 'Wrong data format')
    @api.expect(user_post_model)
    def post(self):
        ## here we get data from scrapper and save it into database
        name = api.payload['name']
        email = api.payload['email']
        ##hashed_password = generate_password_hash(api.payload['passwd'], method='sha256')
        
        hashed_password = ph.hash(api.payload['passwd'])

        new_user = User(public_id=str(uuid.uuid4()), name=name, email=email, hashed_password = hashed_password)

        db.session.add(new_user) 
        db.session.commit()   
        return Response(status=204)

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(public_id=data['public_id']).first()
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
   return decorator 

@api.route('/login', doc={'example': 'login'})
class UserLogin(Resource):
    @api.response(200, 'user logged in')
    @api.response(400, 'Wrong data format')
    @api.expect(login_post_model)
    def post(self):
        ## here we get data from scrapper and save it into database
        email = api.payload['email']
        passwd = api.payload['passwd']
        ## email field in user table should be unique
        user = User.query.filter_by(email = email).first()
        if not user:
            raise NotFound('no user with this email')

        ## unhashed_password = check_password_hash(user.hashed_password, passwd)
        unhashed_password = ph.verify(user.hashed_password, passwd)

        if not unhashed_password:
            raise Forbidden('password incorrect')
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow()+ datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
        
def get_current_user():
    token = request.headers['x-access-tokens']
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    usr = User.query.filter_by(public_id=data['public_id']).first()
    return usr

import logging
@api.route('/books', doc={'example': 'books'})
class ListOwnBooks(Resource):
    @api.response(200, 'user books list')
    @api.response(404, 'No users found')
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user):

        usr = get_current_user()
        db_books = Book.query.filter(Book.user_id == usr.id).all()
        
        if not db_books:
            raise NotFound("books not found")

        books = [BookModel(id = book.id, name = book.name, book_price = book.book_price).to_dict() for book in db_books]
        return {'books': books}


@api.route('/books/add', doc={'example': 'books/add'})
class AddOwnBook(Resource):
    @api.response(200, 'user book added')
    @api.response(404, 'No users found')
    @api.doc(security='apikey')
    @token_required
    @api.expect(book_post_model)
    def post(self, current_user):
        book_name = api.payload['book_name']
        book_price = api.payload['book_price']
        usr = get_current_user()
        new_book = Book(name = book_name, book_price = book_price, user_id = usr.id)
        
        db.session.add(new_book)
        db.session.commit()

        return Response(status=204)


@api.route('/books/favorite/<int:book_id>', doc={'example': 'books/favorite/2'})
class AddFavoriteBook(Resource):
    @api.response(200, 'book added to favorite')
    @api.response(404, 'No users found')
    @api.doc(security='apikey')
    @token_required
    def post(self, current_user, book_id:int):

        usr = get_current_user()
        favorite_book = Book.query.filter(Book.id == book_id).first()  
        if not favorite_book:
            raise NotFound("book not found")
        ## adding the book to the user favorite books   
        usr.favorite_books.append(favorite_book)   
        db.session.add(usr)
        db.session.commit()

        return Response(status=204)

@api.route('/books/favorite', doc={'example': 'books/favorite'})
class UserFavoriteBooks(Resource):
    @api.response(200, 'user favorite books list')
    @api.response(404, 'No users found')
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user):

        usr = get_current_user()

        books = [BookModel(id = book.id, name = book.name, book_price = book.book_price).to_dict() for book in usr.favorite_books]
        return {'favorite books': books}

