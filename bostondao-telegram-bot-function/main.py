# import traceback
# import asyncio
# import requests
# import json 
import os
from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup, Bot
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
 

local = not bool(os.getenv("PRODUCTION"))
if local:
   load_dotenv()

telegram_api_key = os.getenv("TELEGRAM_API_KEY")
print('got key')
print(telegram_api_key)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   """Send a message when the command /start is issued."""
   user = update.effective_user
   await update.message.reply_html(
       rf"Hi {user.mention_html()}!",
       reply_markup=ForceReply(selective=True),
   )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   """Send a message when the command /help is issued."""
   await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   """Echo the user message."""
   await update.message.reply_text(update.message.text)


def initialize_bot():
   # Initialize the bot, add handlers, and return the Application instance.
   application = Application.builder().token(telegram_api_key).build()
   application.add_handler(CommandHandler("start", start))
   application.add_handler(CommandHandler("help", help_command))
   application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
   return application

def main():
   # Create the bot instance and start polling.
   application = initialize_bot()
   #application.run_polling(allowed_updates=Update.ALL_TYPES)
   application.run_polling(allowed_updates=Update.ALL_TYPES, webhook_url=f"http://0.0.0.0:{os.getenv('PORT')}")

   return ("done", 200)

if __name__ == "__main__": # LOCAL TESTING ONLY
   main()
