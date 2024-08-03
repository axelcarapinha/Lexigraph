import config
from dotenv import load_dotenv
import os
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load the API secrets
load_dotenv() 
API_TOKEN = os.getenv('LEXIGRAPH_BOT_TOKEN')
BOT_USERNAME = os.getenv('LEXIGRAPH_BOT_USERNAME')


# Commands
async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass #TODO
    await update.message.reply_text('Start!')

async def command_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Help!')


async def command_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Custom!')



# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower() # ignore case-sentitivity (for an easier interaction)

    if 'hello there' in processed:
        return 'General Kenobi!'
    
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
    app.add_handler(CommandHandler('start', command_custom))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot for incoming requests
    print(f'[INFO] Polling {BOT_USERNAME}''s bot')
    app.run_polling(poll_interval=config.POLL_INTERVAL)