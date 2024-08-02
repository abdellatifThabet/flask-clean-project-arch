from flask import Blueprint
from flask_restx import Api, Namespace
#from flask_app import app


# init the api doc
blueprint_v1 = Blueprint('api', __name__, url_prefix='/api')


app_ns = Namespace('app', ordered=True, validate=True, path='/',
                    description='books management services',
                    security=None)

auth_ns = Namespace('auth', ordered=True, validate=True, path='/',
                    description='authentication services',
                    security=None)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(blueprint_v1, authorizations=authorizations)
api.add_namespace(app_ns)
api.add_namespace(auth_ns)