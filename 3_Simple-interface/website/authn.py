from flask import Blueprint

authn = Blueprint('authn', __name__)


@authn.route('/login')
def login(): # can have a name diff from the route one
    return "<p>Login</p>"

@authn.route('/logout')
def logout():
    return "<p>Logout</p>"

@authn.route('/sign-up')
def sign_up():
    return "<p>Sign_up</p>"
