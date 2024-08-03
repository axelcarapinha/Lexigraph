import config
import os
import json
from api_anki import request, invoke
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.helpers import escape_markdown


# Load the API secrets
load_dotenv() 
API_TOKEN    = os.getenv('LEXIGRAPH_BOT_TOKEN')
BOT_USERNAME = os.getenv('LEXIGRAPH_BOT_USERNAME')


# Commands
async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome! Type "/" to see the available commands')

async def command_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f'''
    Visit {config.URL_LEXIGRAPH_WEBSITE}/home to directly check your account's content
    or {config.URL_LEXIGRAPH_WEBSITE}/about to contact Lexigraph's creator
    '''

    # Ensure URL and text formatting are correct
    escaped_text = escape_markdown(text)

    await update.message.reply_text(escaped_text, parse_mode='MarkdownV2')


#TODO
# async def command_list_decks(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     result = invoke('deckNames')
#     print('[INFO] got list of decks: {}'.format(result))

#     deck_names = ""
#     for deck in result:
        
#     # text = 'Deck created' if result['error'] is None else 'Failure creating deck. Please, try again.'
#     text = 'Deck created'
#     await update.message.reply_text(text)


#TODO consider a mock action for the invoke() method


#TODO
async def command_add_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notes = [{
        "deckName": "test2",
        "modelName": "basic",
        "fields": {
            "Front": "front",
            "Back": "back"
        },
        "tags": [
            "lexigraph"
        ],
        # Uncomment and add details for audio, video, and picture if needed
        # "audio": [{
        #     "url": "your_audio_url",
        #     "filename": "your_audio_filename.mp3",
        #     "skipHash": "your_skip_hash",
        #     "fields": ["Front"]
        # }],
        # "video": [{
        #     "url": "your_video_url",
        #     "filename": "your_video_filename.mp4",
        #     "skipHash": "your_skip_hash",
        #     "fields": ["Back"]
        # }],
        # "picture": [{
        #     "url": "your_picture_url",
        #     "filename": "your_picture_filename.jpg",
        #     "skipHash": "your_skip_hash",
        #     "fields": ["Back"]
        # }]
    }]

    response = invoke('addNotes', notes=notes)
    result = json.loads(response)

    #TODO error message fails!
    text = 'Cards added!' if result.get("error") is None else 'Error adding the cards. Please, try again.'
    await update.message.reply_text(text)

#TODO
async def command_remove_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    invoke('createDeck', deck='test3')
    result = invoke('deckNames')
    print('[INFO] got list of decks: {}'.format(result))
    # text = 'Deck created' if result['error'] is None else 'Failure creating deck. Please, try again.'
    text = 'Deck created'
    await update.message.reply_text(text)



# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower() # ignore case-sentitivity (for an easier interaction)

    if 'hello there' in processed:
        return 'General Kenobi!'
    #TODO
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type # differentiate between a group chat and a private chat
    text: str = update.message.text

    print(f'[INFO] User {update.message.chat.id} in {message_type}: "{text}"')

    # Configure how the bot should respond when in Telegram groups
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text:str = text.replace(BOT_USERNAME, ' ').strip()
            response: str = handle_response(new_text)
        else:
            return # the bot responds in a group ONLY when it has been
    
    else:
        response: str = handle_response(text) # for private chats

    print('[INFO] Bot: ', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'[ERROR] Update {update} caused error {context.error}')





if __name__ == '__main__':
    app = Application.builder().token(API_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', command_start))
    app.add_handler(CommandHandler('help', command_help))
    app.add_handler(CommandHandler('add', command_add_words))
    app.add_handler(CommandHandler('remove', command_remove_words))


    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot for incoming requests
    print(f'[INFO] Polling {BOT_USERNAME}''s bot')
    app.run_polling(poll_interval=config.POLL_INTERVAL)