# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

import copy
import connectors
import telegram
import telegram.ext as ext
import requests
import logging
import os
from connectors import oxford_api, users

REVIEW, CONFIRMATION = range(2)
_BROADCAST_MESSAGE_ = None

def main(dispatcher):
    send_broadcast_handler = ext.ConversationHandler(
        entry_points=[ext.CommandHandler('send_broadcast', __send_broadcast)],

        states={
            REVIEW: [ext.MessageHandler(ext.Filters.text, __review_message)],
            CONFIRMATION: [ext.MessageHandler(ext.Filters.regex('Yes|No'), __confirm_broadcast)]
        },

        fallbacks=[ext.CommandHandler('cancel', __send_broadcast_cancel)]
    )
    
    dispatcher.add_handler(send_broadcast_handler)
    
def __send_broadcast(bot, update):
    global _BROADCAST_MESSAGE_
    _BROADCAST_MESSAGE_ = ''

    next_state = ext.ConversationHandler.END

    if connectors.authentication.check_authorization(
            update.message.from_user.id):
        update.message.reply_text("Send me the message you want to broadcast")
        next_state = REVIEW
    else:
        update.message.reply_text("Sorry but you don't have enough priviledges to send a broadcast message")

    return next_state

def __review_message(bot, update):
    global _BROADCAST_MESSAGE_

    _BROADCAST_MESSAGE_ = update.message.text_markdown

    update.message.reply_markdown("{}\n\nThat message is about to be sent to all registered users. Are you sure? (Yes/No)"
                                .format(_BROADCAST_MESSAGE_))

    return CONFIRMATION

def __confirm_broadcast(bot, update):
    global _BROADCAST_MESSAGE_

    confirmation = update.message.text

    if confirmation.lower() == "yes":
        for user in users.get_all_users():
            bot.sendMessage(
                chat_id=user['chat_id'],
                text=_BROADCAST_MESSAGE_,
                parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        update.message.reply_text("No message will be sent")
            

    return ext.ConversationHandler.END

def __send_broadcast_cancel(bot, update):
    global _BROADCAST_MESSAGE_

    _BROADCAST_MESSAGE_ = None

    update.message.reply_text("No message will be sent")

    return ext.ConversationHandler.END
