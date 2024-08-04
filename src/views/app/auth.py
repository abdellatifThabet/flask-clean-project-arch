from flask_restx import fields

from src.db_models import User
from src.views.blueprint import api, auth_ns
from src.views.resources import ResourceApp
from src.views import json_response

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

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

# refresh_token_model = auth_ns.model('refresh_token_model', {
#     'token': fields.String(required=True, description='name of the user')
# })

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
        
        
        
############
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID", ""),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET", ""),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)



@app.route('/google_auth')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    userinfo = resp.json()
    session["email"] = userinfo["email"]
    session["name"] = userinfo["name"]
    # do something with the token and profile
    return redirect('/')

@app.route('/')
def hello():
    email = dict(session).get("email", None)
    name = dict(session).get("name")
    session.pop("email")
    return f"hello world {email} .having name. {name}"