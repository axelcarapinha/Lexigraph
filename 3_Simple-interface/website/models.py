import config
from . import db # importing from the __init__.py
from flask_login import UserMixin 
from sqlalchemy.sql import func # for func.now()
from sqlalchemy.types import JSON

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True) # has autoincrement (default)
    data = db.Column(db.String(config.MAX_LEN_WORD))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    word_info = db.Column(JSON)
    card_notes = db.Column(JSON)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(config.MAX_LEN_EMAIL), unique=True)
    password = db.Column(db.String(config.MAX_LEN_PASSWORD))
    username = db.Column(db.String(config.MAX_LEN_USERNAME))
    words = db.relationship('Word') # SQLAlchemy needs a capital key in this case
    occupation = db.Column(db.String(config.MAX_LEN_OCCUPATION))