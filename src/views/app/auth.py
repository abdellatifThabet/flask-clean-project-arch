from flask_restx import fields
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from src.db_models import User
from src.views.blueprint import api, auth_ns
from src.views.resources import ResourceApp
from src.views import json_response


#from werkzeug.security import generate_password_hash,check_password_hash
## as a hash function we'll be  using argon
from argon2 import PasswordHasher
ph = PasswordHasher()
import uuid

from flask_app import app, db
from flask import url_for, session, redirect
from authlib.integrations.flask_client import OAuth
import os


user_post_model = auth_ns.model('user_post_model', {
    'name': fields.String(required=True, description='name of the user', default='user 1'),
    'email': fields.String(required=True, description='email of the user', default='user1@gmail.com'),
    'passwd': fields.String(required=True, description='password of the facebook account', default='54460380'),
})

login_post_model = auth_ns.model('login_post_model', {
    'email': fields.String(required=True, description='name of the user'),
    'passwd': fields.String(required=True, description='password of the facebook account', format='password'),
})


@auth_ns.route('/register', doc={'example': 'register'})
class UserManagement(ResourceApp):
    @auth_ns.expect(user_post_model)
    def post(self):
        name = api.payload['name']
        email = api.payload['email']
        passwd = api.payload['passwd']
        user = User.get_user_by_email(email)
        if user:
            return json_response(status_code=409, data={"message": "user already exists"})
        new_user = User(public_id=str(uuid.uuid4()), email=email, name=name)
        new_user.set_password(passwd=passwd)
        new_user.save()
        return json_response(status_code=204, data={"message": "user resgitered"})

@auth_ns.route('/login', doc={'example': 'login'})
class UserLogin(ResourceApp):
    @auth_ns.expect(login_post_model)
    def post(self):
        ## here we get data from scrapper and save it into database
        email = api.payload['email']
        passwd = api.payload['passwd']
        ## email field in user table should be unique
        user = User.get_user_by_email(email=email)
        if user and user.check_password(passwd):
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            return json_response(status_code=200, data={
                "message": "tokens generated",
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }})
        return json_response(status_code=400, trace={"error": "invalid username or password"})

@auth_ns.route('/refresh', doc={'example': 'refresh'})
class UserRefresh(ResourceApp):
    @auth_ns.doc(security='apikey')
    @jwt_required(refresh=True)
    def get(self):
        identity = get_jwt_identity()

        new_acces_token = create_access_token(identity = identity)
        new_refresh_token = create_refresh_token(identity = identity)

        return json_response(status_code=200, data={
            "message": "tokens generated from refresh",
            "tokens": {
                "access_token": new_acces_token,
                "refresh_token": new_refresh_token
            }})