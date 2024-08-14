# "authn" == authentication (used here)
# "authz" == authorization

import config  
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

authn = Blueprint('authn', __name__)

@authn.route('/login', methods=['GET', 'POST'])
def login(): # can have a name diff from the one of the route
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password') 

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) # "remember" stores the session data
                return redirect(url_for('views.home'))
            else:    
                flash('Incorrect password. Pleasy, try again.', category='error')
        else:
            flash('Email does NOT exist.', category='error')

    return render_template("login.html", user=current_user)

@authn.route('/logout')
@login_required # used WHEREVER there's a redirect for the home page (or someone could bypass authn)
def logout():
    logout_user()
    return redirect(url_for("authn.login")) 

@authn.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password_first = request.form.get('passwordFirst')
        password_confirmation = request.form.get('passwordConfirmation')
        occupation = request.form.get('occupation')

        user = User.query.filter_by(email=email).first() 

        #TODO add more sanizitization (for the occupation, for example)
        # Sanitize user data
        if user:
            flash('Email already in use.', category='error')
        elif len(email) < config.MIN_LEN_EMAIL:
            flash(f'Email must be greather than {config.MIN_LEN_EMAIL - 1} characters.', category='error')
        elif len(username) < config.MIN_LEN_USERNAME:
            flash(f'First name should have at least {config.MIN_LEN_USERNAME} characters.', category='error')
        elif password_first != password_confirmation:
            flash('Passwords do NOT match.', category='error')
        elif len(password_first) < config.MIN_LEN_PASSWORD: #TODO add more rules and tips for the password field
            flash(f'Password should have at least {config.MIN_LEN_PASSWORD} characters.', category='error')
        elif len(occupation) < config.MIN_LEN_OCCUPATION:
            flash(f'Occupation should have at least {config.MIN_LEN_OCCUPATION} characters.', category='error')
        elif len(occupation) > config.MAX_LEN_OCCUPATION:
            flash(f'Occupation cannot have more than {config.MAX_LEN_OCCUPATION} characters.', category='error')
        else: # add user to the database
            '''
            (1) Unique salt is generated (wth a pseudo-random function)
            (2) PBKDF2 (Password-Based Key Derivation Function 2) derives a key 
                from a password using a pseudorandom function, 
                such as HMAC (Hash-based Message Authentication Code) with SHA-256
            (3) Iterative hashing: PBKDF2 applies the pseudorandom function multiple times (iterations),
                which increases the computational cost to perform brute-force attacks on the hashed password.
            '''
            new_user = User(email=email, username=username, password=generate_password_hash(password_first, method='pbkdf2:sha256'), occupation=occupation)

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash("Account creation successfull. Welcome!", category='success')
            return redirect(url_for('views.home')) # finding the URL associating with this function
            
    return render_template("sign_up.html", user=current_user)