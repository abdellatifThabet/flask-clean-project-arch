from flask_restx import fields

from src.db_models import Book, User
from src.models import BookModel
from src.views.blueprint import api, app_ns, auth_ns
from src.views.resources import ResourceApp
from src.views import json_response

from flask_jwt_extended import jwt_required, get_jwt_identity

#from werkzeug.security import generate_password_hash,check_password_hash
## as a hash function we'll be  using argon
from argon2 import PasswordHasher
ph = PasswordHasher()
from functools import wraps
import uuid
import jwt
import datetime
from werkzeug.exceptions import NotFound, Forbidden

from flask_app import app, db
from src.views.app import auth

from src.lib.app.user import get_all_books, create_book, add_favorite_book, get_favorite_books

import logging
logger = logging.getLogger(__name__)

book_post_model = app_ns.model('book_post_model', {
    'book_name': fields.String(required=True, description='name of the book'),
    'book_price': fields.Integer(required=True, description='price of the book'),
})


@app_ns.route('/books', doc={'example': 'books'})
class ListOwnBooks(ResourceApp):
    @app_ns.doc(security='apikey')
    @jwt_required()
    def get(self):
        user_email = get_jwt_identity()
        status_code, data = get_all_books(user_email)

        if status_code == 200:
            return json_response(status_code=status_code, data=data)
        elif status_code == 404:
            return json_response(status_code=status_code, trace=data["trace"])
        else:
            return json_response(status_code=500, trace="internal server error")



@app_ns.route('/books/add', doc={'example': 'books/add'})
class AddOwnBook(ResourceApp):
    @app_ns.expect(book_post_model)
    @app_ns.doc(security='apikey')
    @jwt_required()
    def post(self):
        user_email = get_jwt_identity()
        status_code, data = create_book(api.payload, user_email)
        if status_code == 204:
            return json_response(status_code=status_code, data=data)
        elif status_code == 404:
            return json_response(status_code=status_code, trace=data)
        else:
            return json_response(status_code=500, trace="internal server error")



@app_ns.route('/books/favorite/<int:book_id>', doc={'example': 'books/favorite/2'})
class AddFavoriteBook(ResourceApp):
    @app_ns.doc(security='apikey')
    @jwt_required()
    def post(self, book_id:int):

        user_email = get_jwt_identity()
        status_code, data = add_favorite_book(user_email, book_id)
        if status_code == 200:
            return json_response(status_code=status_code, data=data)
        elif status_code == 404:
            return json_response(status_code=status_code, trace=data)
        else:
            return json_response(status_code=500, trace="internal server error")


@app_ns.route('/books/favorite', doc={'example': 'books/favorite'})
class UserFavoriteBooks(ResourceApp):
    @app_ns.doc(security='apikey')
    @jwt_required()
    def get(self):

        user_email = get_jwt_identity()
        status_code, data = get_favorite_books(user_email)
        if status_code == 200:
            return json_response(status_code=status_code, data=data)
        else:
            return json_response(status_code=500, trace="internal server error")






















# @app_ns.route('/register', doc={'example': 'register'})
# class UserManagemet(ResourceApp):
#     @app_ns.response(200, 'user added')
#     @app_ns.response(400, 'Wrong data format')
#     @app_ns.expect(user_post_model)
#     def post(self):
#         ## here we get data from scrapper and save it into database
#         name = api.payload['name']
#         email = api.payload['email']
#         ##hashed_password = generate_password_hash(api.payload['passwd'], method='sha256')
        
#         hashed_password = ph.hash(api.payload['passwd'])

#         new_user = User(public_id=str(uuid.uuid4()), name=name, email=email, hashed_password = hashed_password)

#         db.session.add(new_user) 
#         db.session.commit()   
#         return Response(status=204)

# def token_required(f):
#    @wraps(f)
#    def decorator(*args, **kwargs):
#        token = None
#        if 'x-access-tokens' in request.headers:
#            token = request.headers['x-access-tokens']
 
#        if not token:
#            return jsonify({'message': 'a valid token is missing'})
#        try:
#            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#            current_user = User.query.filter_by(public_id=data['public_id']).first()
#        except:
#            return jsonify({'message': 'token is invalid'})
 
#        return f(current_user, *args, **kwargs)
#    return decorator 

# @app_ns.route('/login', doc={'example': 'login'})
# class UserLogin(ResourceApp):
#     @app_ns.response(200, 'user logged in')
#     @app_ns.response(400, 'Wrong data format')
#     @app_ns.expect(login_post_model)
#     def post(self):
#         ## here we get data from scrapper and save it into database
#         email = api.payload['email']
#         passwd = api.payload['passwd']
#         ## email field in user table should be unique
#         user = User.query.filter_by(email = email).first()
#         if not user:
#             raise NotFound('no user with this email')

#         ## unhashed_password = check_password_hash(user.hashed_password, passwd)
#         unhashed_password = ph.verify(user.hashed_password, passwd)

#         if not unhashed_password:
#             raise Forbidden('password incorrect')
#         token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow()+ datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])
#         return jsonify({'token': token})
        
# def get_current_user():
#     token = request.headers['x-access-tokens']
#     data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#     usr = User.query.filter_by(public_id=data['public_id']).first()
#     return usr