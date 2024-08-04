import config
import os
import json
import requests
from api_anki import request, invoke
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.helpers import escape_markdown
from api_request import api_request_info_word


# Load the API secrets
load_dotenv() 
API_TOKEN    = os.getenv('LEXIGRAPH_BOT_TOKEN')
BOT_USERNAME = os.getenv('LEXIGRAPH_BOT_USERNAME')
#TODO consider a mock action for the invoke() method


# Commands
async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome! Type "/" to see the available commands')

async def command_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Prepare the needed URLs
    URL_HOME  = f"{config.URL_LEXIGRAPH_WEBSITE}/home"
    URL_ABOUT = f"{config.URL_LEXIGRAPH_WEBSITE}/about"
    text = f"Check [your account's content]({URL_HOME})\n or [contact Lexigraph's creator]({URL_ABOUT})."
    URL_TELEGRAM_API = "https://api.telegram.org/bot{}/sendMessage".format(context.bot.token)

    # Make the JSON for the clickable URL API request
    chat_id = update.message.chat_id
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "markdown"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(URL_TELEGRAM_API, json=payload, headers=headers)
    
    # Confirm success of the request to Telegram's API
    if response.status_code == 200:
        print("[INFO] [CMD HELP] Message sent successfully")
    else:
        print(f"[INFO] [CMD HELP] Failed to send message: {response.status_code} - {response.text}")

    await update.message.reply_text(response)

async def add_word_to_deck(input_user_context, input_word):
    # Create a dialg and meaning with that word
    # TODO: Replace with actual API request
    word_obj = api_request_info_word(input_user_context, input_word)

    # Extract dialog parts from the word object
    dialog_parts = word_obj.get('dialog', [])

    # Create the ANKI card
    deck_name = "test1" #TODO change this
    model_name = "basic"
    front_text = f"{input_word}"

    # Generate the HTML content for the card's back
    back_text = f'''
    <ul>
        <li> 
            <u>Word</u>: {input_word}
            <br>
            <u>Meaning</u>: {word_obj.get('definition', 'No definition available')}
            <br>
            <ul>
    '''
    
    # Add dialog parts to the HTML for the card
    for i, dialog_part in enumerate(dialog_parts):
        back_text += f'''
                <!-- PART {i + 1} / {len(dialog_parts)} -->
                <li>
                    <strong>Bob:</strong>   {dialog_part.get('person1', 'No text available')}
                    <br>
                    <strong>Alice:</strong> {dialog_part.get('person2', 'No text available')}
                    <br>
                </li>
        '''
    back_text += '''
            </ul>
        </li>
    </ul>
    '''

    tags = ["lexigraph"]
    audio_url = "url_audio"
    audio_filename = "filename_audio.mp3"
    video_url = "url_video"
    video_filename = "filename_video.mp4"
    picture_url = "url_picture"
    picture_filename = "filename_pictre.jpg"

    # Build the JSON for the card
    notes = [{
        "deckName": deck_name,
        "modelName": model_name,
        "fields": {
            "Front": front_text,
            "Back": back_text
        },
        "tags": tags,
        # "audio": [{
        #     "url": url_audio,
        #     "filename": filename_audio,
        #     "skipHash": "skip_hash",  
        #     "fields": ["Front"]
        # }],
        # "video": [{
        #     "url": url_video,
        #     "filename": filename_video,
        #     "skipHash": "skip_hash",  
        #     "fields": ["Back"]
        # }],
        # "picture": [{
        #     "url": url_picture,
        #     "filename": filename_picture,
        #     "skipHash": "skip_hash", 
        #     "fields": ["Back"]
        # }]
    }]

    # Send request to AnkiConnect's API (to add the card to the deck)
    response = invoke('addNotes', notes=notes)
    result = json.loads(response) #TODO backup that JSON file (if ANKI does NOT export that)

    # Handle the response
    text = '[INFO] [CMD ADD] Cards added!' if result.get("error") is None else '[ERROR] [CMD ADD] adding the cards. Please, try again.'
    print(text)

    return text

async def command_add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the desired word and its meaning
    if len(context.args) < 2:
        await update.message.reply_text("Please provide both context and a word. Example usage: /add NetworkEngineerSecurity Passion")
        print("[ERROR] [CMD ADD] Insufficient arguments provided.")
        return

    input_user_context = context.args[0]
    input_word = ' '.join(context.args[1:])

    # Check for validation
    if not input_user_context or not input_word:
        await update.message.reply_text("Both word and meaning are required.")
        print("[ERROR] [CMD ADD] Word or meaning is missing.")
        return
    elif ' ' in input_user_context:
        await update.message.reply_text("Please provide a single word.")
        print("[ERROR] [CMD ADD] User probably tried to input more than one word.")
        return

    text = await add_word_to_deck(input_user_context, input_word)
    await update.message.reply_text(text)

#TODO
async def command_remove_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    invoke('createDeck', deck='test3')
    result = invoke('deckNames')
    print('[INFO] got list of decks: {}'.format(result))
    # text = 'Deck created' if result['error'] is None else 'Failure creating deck. Please, try again.'
    text = 'Deck created'
    await update.message.reply_text(text)

# Handlers
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.document.file_id
    try:
        file_content = get_file(file_id, context.bot.token)
    except FileNotFoundError as e:
        print("[ERROR]", e)
        await update.message.reply_text("Failed to process the file. Please, try again.")
        return

    words = file_content.splitlines()
    user_context = 'CyberSecurityAndComputerNetworks' #TODO pass by argument
    for word in words:
        # print(word)
        await add_word_to_deck(user_context, word)

    await update.message.reply_text('Words from the file added')
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type # differentiate between a group chat and a private chat
    text: str = update.message.text
    print(f'[INFO] User {update.message.chat.id} in {message_type}: "{text}"')

    # Bot's behaviour in Telegram groups
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text:str = text.replace(BOT_USERNAME, ' ').strip()
            response: str = customized_response(new_text)
        else:
            return # the bot responds in a group ONLY when it has been called (with the @)
    else:
        response: str = customized_response(text) # for private chats

    if response:  # avoid sending an empty response
        print('[INFO] Bot: ', response)
        await update.message.reply_text(response, parse_mode='MarkdownV2')
    else:
        print('[WARNING] No response generated for the text:', text)



# Utils
def get_file(file_id, token):
    URL_TELEGRAM_API = f"https://api.telegram.org/bot{token}/getFile"
    response = requests.get(URL_TELEGRAM_API, params={'file_id': file_id})
    json_response = response.json()
    if response.status_code != 200 or not json_response.get('ok'):
        raise FileNotFoundError("[ERROR] Failed to get the file info from Telegram")

    file_path = json_response['result']['file_path']
    get_file_content_api_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
    response = requests.get(get_file_content_api_url)
    if response.status_code != 200:
        raise FileNotFoundError("[ERROR] Failed to download the file content from Telegram")

    return response.content.decode('utf-8')

def customized_response(text: str) -> str:
    processed: str = text.lower() # ignore case-sentitivity (for an easier interaction)

    print(processed)

    # Making the bot respond in Markdown to some movie references
    if 'hello there' in processed:
        return '_General Kenobi\\!_  \n\\(Star Wars\\, Episode III\\)' # 2 spaces + 1 newline = 1 newline (Markdown)
    elif 'after all this time' in processed:
        return '_Always_\\.  \n\\(Harry Potter and the Deathly Hallows\\: Part 2\\)'
    elif 'are you serious' in processed:
        return '_I am always serious\\. I just have a very good poker face\\._  \n\\(Interstellar\\, TARS\\)'
    elif 'make a joke' == processed:
        return '_Self destruct sequence in T minus 10\\, 9\\.\\.\\._  \n\\(Interstellar\\, TARS\\)'
    else:
        return 'I did _not_ understand that\\, sorry\\.  \nPlease\\, provide other messages or commands\\.'



# Errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'[ERROR] Update {update} caused error {context.error}')



if __name__ == '__main__':
    app = Application.builder().token(API_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', command_start))
    app.add_handler(CommandHandler('help', command_help))
    app.add_handler(CommandHandler('add', command_add_word))
    app.add_handler(CommandHandler('remove', command_remove_words))

    # Generic handlers
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file)) 

    # Errors
    app.add_error_handler(error)

    # Polls the bot for incoming requests
    print(f'[INFO] Polling {BOT_USERNAME}''s bot')
    app.run_polling(poll_interval=config.POLL_INTERVAL)