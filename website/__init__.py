# The __init__.py filename defines the 'website' folder as a Python package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'huasduofhaosudfhas' #TODO how to NOT disclose this private key

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) 

    from .views import views
    from .authn import authn

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(authn, url_prefix='/')

    from .models import User, Word
    create_database(app)
    
    # Defining to Flask how to LOAD a user
    login_manager = LoginManager()
    login_manager.login_view = 'authn.login' # where users go if NOT loged-in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # "int()" because we used the primary key as an Integer

    return app


def create_database(app):
    with app.app_context():  # ensuring we are within our 'app' contxt
        if not path.exists('website/' + DB_NAME):
            db.create_all() 
            print('[INFO] Database created.')