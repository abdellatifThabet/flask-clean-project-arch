import unittest
from flask_app import app, db
import base64


from flask import url_for

def list_routes(app):
    for rule in app.url_map.iter_rules():
        print(rule)

class BaseTest(unittest.TestCase):

    def setUp(self) -> None:

        self.test_client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        list_routes(app)


    def tearDown(self) -> None:
        db.session.rollback()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()