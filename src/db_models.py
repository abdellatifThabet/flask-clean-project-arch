from enum import unique
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
 
db = SQLAlchemy()
jwt = JWTManager()


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

    def __init__(self, public_id, name, email):
        self.public_id = public_id
        self.name = name
        self.email = email
            
    def __repr__(self):
        return f"<User {self.name}>"
    
    def set_password(self, passwd):
        self.hashed_password = generate_password_hash(passwd)
        
    def check_password(self, passwd):
        return check_password_hash(self.hashed_password, passwd)
    
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
        
    def save(self):
        db.session.add(self)
        db.session.commit()
            
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        

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


