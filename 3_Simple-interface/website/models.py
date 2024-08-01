import config
from . import db # importing from the __init__.py
from flask_login import UserMixin 
from sqlalchemy.sql import func # for the func.now()

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True) # has autoincrement (default)
    data = db.Column(db.String(config.MAX_LEN_WORD))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

#TODO (or consider using the AnkiWeb API)
# class SpacedRepetition()


#TODO confirm some values (max number of chars for email, ...)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(config.MAX_LEN_EMAIL), unique=True)
    password = db.Column(db.String(config.MAX_LEN_PASSWORD))
    username = db.Column(db.String(config.MAX_LEN_USERNAME))
    words = db.relationship('Word') # SQLAlchemy needs a capital key in this case