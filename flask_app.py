from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from config_app import config
from src.db_models import db as db_model, jwt
from src.db_models import User


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)

    db_model.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db_model)
    
    # the blueprint import should be here after flask app initialization
    from src.views.blueprint import blueprint_v1
    app.register_blueprint(blueprint_v1)

    # load user
    @jwt.user_lookup_loader 
    def user_lookup_callback(_jwt_headers, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(email = identity).one_or_none()
    
    # jwt error handler
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "token has expired",
                        "error": "token expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "signature verification failed",
                        "error": "invalid check"}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "request does not contain a valid token",
                        "error": "auth header"}), 401
        
    return app, db_model

app, db  = create_app()