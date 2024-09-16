import logging
import os


class ConfigApp(object):
    # generic
    CSRF_ENABLED = os.environ.get('CSRF_ENABLED', False)
    API_KEY = os.environ['API_KEY']

    DEBUG = os.environ.get('DEBUG', False)
    TESTING = os.environ.get('TESTING', False)
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', logging.NOTSET)

    # swagger
    SWAGGER_UI_DOC_EXPANSION = 'list'

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = ConfigApp()
