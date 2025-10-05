#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import random

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# my list
grocery_list = []
profile = {}

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Type /help for instructions"
)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "add ____ to add groceries \
        \nremove ____ to remove groceries \
        \nlist ____ to view current list \
        \ndone ____ to clear grocery list" )



async def listhandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """The grocery list"""
    msg = update.message.text
    user = update.effective_user
    firstword = msg.split()[0].lower()

    

    # For logs
    print(user["username"] + ":", msg)

    # Add to list

    if firstword == "add":
        parts = msg.split(' ',1)

        if len(parts) > 1:
            item = parts[1].strip()

            
            if len(parts[1]) >= 25:
                await update.message.reply_text("Too many characters.")
            
            elif len(parts) == 0: 
                await update.message.reply_html("You didnt write anything.")

            elif item not in grocery_list:
                grocery_list.append(item)
                await update.message.reply_text(f"Added {item}")

            elif item in grocery_list:
                await update.message.reply_html("Item already in grocery list")

    elif firstword == "done": 
        grocery_list.clear()
        await update.message.reply_html("Grocery list cleared.")
    
    elif firstword == "remove":
        parts = msg.split(' ', 1)

        if len(parts) > 1:
            
            item = parts[1].strip()
            print(item)

            if len(parts[1]) > 25:
                await update.message.reply_html("Too many characters")
                print(1)
                
             
            elif len(parts[1]) == 0: 
                ("You didnt write anything.")
                print(2)
            elif item in grocery_list:
                grocery_list.remove(item)
                await update.message.reply_html(f"{item} was removed")
                print(3)
            elif item not in grocery_list:
                await update.message.reply_html("Item not in list")
                print(4)
            


    
    elif msg.lower().startswith("list"):
        if len(grocery_list) == 0:
            await update.message.reply_text("Grocery list is empty")
        else:
            await update.message.reply_text(grocery_list)

    # elif firstword == "join":
    #     profile = msg
        
    






def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("8102123985:AAFcIfgoPt4bs_bOtjOBfGp5vflSerZ-iRY").build()


    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, listhandler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main() 