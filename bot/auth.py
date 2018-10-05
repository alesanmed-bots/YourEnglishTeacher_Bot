# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

from connectors import authentication
import telegram.ext as ext

def main(dispatcher):
    auth_handler = ext.CommandHandler('auth', auth)
    dispatcher.add_handler(auth_handler)

def auth(bot, update):
    message = update.message
    chat_id = message.chat.id
    user_id = message.from_user.id

    token = update.message.text.replace('/auth ', '')

    if authentication.auth_user(user_id, token):
        bot.sendMessage(chat_id=chat_id, text='Authentication successful, you can now use private commands')
    else:
        bot.sendMessage(chat_id=chat_id, text='Invalid token, please try again')
