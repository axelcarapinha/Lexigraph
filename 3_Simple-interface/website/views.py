import config
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Word
import json

from .api_request import api_request_info_word

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        word = request.form.get('word')

        if len(word) < config.MIN_LEN_WORD:
            flash('Word is too short.', category='error')
        else: # provide the schema for the note and add to the database
            new_word = Word(data=word, user_id=current_user.id, word_info=api_request_info_word(current_user.id, word)) 
            #TODO consider using threads

            db.session.add(new_word)
            db.session.commit() # analog to the commit of PostgreSQL
            flash('Word added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-word', methods=['POST'])
def delete_word():
    word = json.loads(request.data)
    wordId = word['wordId'] #TODO consider if here
    word = Word.query.get(wordId)
    if word:
        if word.user_id == current_user.id:
            db.session.delete(word)
            db.session.commit()

    return jsonify({}) # an empty response 
    