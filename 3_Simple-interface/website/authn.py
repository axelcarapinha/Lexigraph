import config  
from flask import Blueprint, render_template, request, flash

authn = Blueprint('authn', __name__)

@authn.route('/login', methods=['GET', 'POST'])
def login(): # can have a name diff from the route one
    data = request.form # ALL the info sent from the form
    print(data) 
    return render_template("login.html")

@authn.route('/logout')
def logout():
    return render_template("home.html")

@authn.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password_first = request.form.get('passwordFirst')
        password_confirmation = request.form.get('passwordConfirmation')

        if len(email) < config.MIN_LEN_EMAIL:
            flash(f'Email must be greather than {config.MIN_LEN_EMAIL - 1} characters.', category='error')
        elif len(username) < config.MIN_LEN_USERNAME:
            flash(f'First name should be greather than {config.MIN_LEN_USERNAME - 1} characters.', category='error')
        elif password_first != password_confirmation:
            flash('Passwords do NOT match.', category='error')
        elif len(password_first) < config.MIN_LEN_PASSWORD: #TODO add more rules and tips for the password field
            flash(f'Password should have at least {config.MIN_LEN_PASSWORD - 1} characters.', category='error')
        else:
            flash("Account creation SUCCESSFUL", category='success')
            # add user to database


    return render_template("sign_up.html")
