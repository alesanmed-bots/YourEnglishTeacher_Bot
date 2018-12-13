# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

from connectors import users
from connectors import words
import telegram
from utils import word_utils

def send_daily_message(bot):
    users_to_send = users.get_all_users()

    daily_word = words.get_daily_word()

    for user in users_to_send:
        word_utils.send_daily_word(daily_word, user['chat_id'], bot)