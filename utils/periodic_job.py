# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

from connectors import users
from connectors import words

def send_daily_message(bot):
    users_to_send = users.get_all_users()

    daily_word = words.get_daily_word()

    for user in users_to_send:
        bot.sendMessage(chat_id=user['chat_id'], text='%s - %s' % (daily_word['word'], daily_word['meaning']))