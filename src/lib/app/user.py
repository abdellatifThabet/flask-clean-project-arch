from src.db_models import Book, User
from flask_app import db

from src.views import json_response
from typing import Tuple, Dict

from src.utils.serializers.book_serializers import BookSchema   

def get_all_books(user_email)-> Tuple[int, Dict]:
    usr = User.query.filter_by(email=user_email).first()
    if not usr:
        return 404, {"trace": "no valid users"}
        
    db_books = Book.query.filter(Book.user_id == usr.id).all()

    # in recent marshamllow version only when result is returned
    # and in case of errors an exception will occur
    try:    
        serialized_data = BookSchema(many=True).dump(db_books)
    except:
        return 500, 
    data = {"books": serialized_data}
    return 200, data


def create_book(payload, user_email)-> Tuple[int, Dict]:
        book_name = payload['book_name']
        book_price = payload['book_price']
        
        usr = User.query.filter_by(email=user_email).first()
        if not usr:
            return 404, "no valid users"
        
        new_book = Book(name = book_name, book_price = book_price, user_id = usr.id)
        
        db.session.add(new_book)
        db.session.commit()
        return 204, {"message": "book added"}
    

def add_favorite_book(user_email, book_id)-> Tuple[int, Dict]:
    usr = User.query.filter_by(email=user_email).first()
    favorite_book = Book.query.filter(Book.id == book_id).first()  
    if not favorite_book:
        return 404, {"trace": "book not found"}
    ## adding the book to the user favorite books   
    usr.favorite_books.append(favorite_book)   
    db.session.add(usr)
    db.session.commit()
    return 200, {"message": "book added to favorite"}


def get_favorite_books(user_email)-> Tuple[int, Dict]:
    usr = User.query.filter_by(email=user_email).first()

    try:    
        serialized_data = BookSchema(many=True).dump(usr.favorite_books)
    except:
        return 500, 
    return 200, {"favorite_books": serialized_data}
