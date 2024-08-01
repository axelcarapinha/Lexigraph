# The __init__.py filename defines the 'website' folder as a Python package

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'huasduofhaosudfhas' #TODO how to NOT disclose this private key for the sessions (tokens, and more)

    from .views import views
    from .authn import authn

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(authn, url_prefix='/')

    return app



