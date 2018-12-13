# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

import connectors.words as words
from utils import word_utils
import telegram
import telegram.ext as ext

def main(dispatcher):
    get_first_word_handler = ext.CommandHandler('get_first_word', get_first_word)
    dispatcher.add_handler(get_first_word_handler)

def get_first_word(bot, update):
    word = words.get_first_word()

    word_utils.send_daily_word(word, update.message.from_user.id, bot)
