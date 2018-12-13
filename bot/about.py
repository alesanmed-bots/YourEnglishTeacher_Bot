# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

from connectors import users
from telegram.ext import CommandHandler

def main(dispatcher):
    about_handler = CommandHandler('about', __about)
    dispatcher.add_handler(about_handler)
    
def __about(bot, update):
    update.message.reply_html(
        ('This bot has been developed by @alesanmed. '
        'If you are a user and have any problem, you '
        'can contact him for resolving it. If you are '
        'a developer and want to contribute to the bot, '
        'please refer to the bot '
        '<a href="https://github.com/alesanmed/YourEnglishTeacher_Bot">GitHub repository</a>.')
    )