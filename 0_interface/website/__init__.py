# The __init__.py filename defines the 'website' folder as a Python package
import config
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from applicationinsights.flask.ext import AppInsights
from logging import StreamHandler

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.SERVER_SECRET_KEY
    # app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = config.AZURE_INSTRUMENTATION_KEY

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.DATABASE_NAME}'
    db.init_app(app) 

    # Logging - Azure Aplication Insights integration
    # appinsights = AppInsights(app)
    # @app.after_request # Force flushing application insights handler after each request
    # def after_request(response):
    #     appinsights.flush()
    #     return response
    
    # # Logging - Keep having output (and NOT just logs)
    # streamHandler = StreamHandler()
    # app.logger.addHandler(streamHandler)

    # # Logging - Enable INFO logging (to capture when a new user enters)
    # app.logger.setLevel(logging.DEBUG)

    # # Logging - Apply the same formatter on ALL log handlers
    # for logHandler in app.logger.handlers:
    #     logHandler.setFormatter(logging.Formatter('[FLASK-SAMPLE][%(levelname)s]%(message)s'))

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
        if not path.exists('website/' + config.DATABASE_NAME):
            db.create_all() 
            print('[INFO] Database created.')