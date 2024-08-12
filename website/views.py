import config
import json
from flask import current_app as app
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Word
from .api_request import api_request_info_word
from .api_anki import api_anki_get_card_notes

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    app.logger.info('A new user arrived.') # prompts the Ollama's VM to start running

    if request.method == 'POST':
        word = request.form.get('word')

        if len(word) < config.MIN_LEN_WORD:
            flash('Word is too short.', category='error')
            return redirect(url_for('views.home'))  # Redirect to the same page without flag

        # Create a dialog from the word
        word_info  = api_request_info_word(current_user.occupation, word)
        card_notes = api_anki_get_card_notes(word, word_info)

        # Add to the known cards of the user
        new_word = Word(data=word, user_id=current_user.id, word_info=word_info, card_notes=card_notes)
        db.session.add(new_word)
        db.session.commit()

        flash('Word added!', category='success')

        # Redirect with a query parameter indicating success
        return redirect(url_for('views.home', reloaded='true'))

    # Power Up the VM with an Azure's Runbook (because it's a GET request)
    return render_template("home.html", user=current_user)


@views.route('/delete-word', methods=['POST'])
def delete_word():
    word = json.loads(request.data)
    wordId = word['wordId'] 
    word = Word.query.get(wordId)
    if word:
        if word.user_id == current_user.id:
            db.session.delete(word)
            db.session.commit()

    return jsonify({}) # an empty response

@views.route('/get-card-notes/<int:word_id>', methods=['GET'])
@login_required
def get_card_notes(word_id):
    word = Word.query.get(word_id)
    if word and word.user_id == current_user.id:
        return jsonify({
            'card_notes': word.card_notes,
            'word': word.data
        })
    return jsonify({'error': 'Word not found or access denied'}), 404

@views.route('/about', methods=['GET'])
def about():
    return redirect(config.URL_ABOUT_PAGE)