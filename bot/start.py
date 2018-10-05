# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

from connectors import users
from telegram.ext import CommandHandler

def main(dispatcher):
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
def start(bot, update):
    users.register_user(update.message.from_user.id, update.message.from_user.username, update.message.chat.id)
    bot.send_message(chat_id=update.message.chat_id, text="I'm YourEnglishTeacher. I will daily send you useful words so you can improve your english.")