# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

import connectors.words as words
import telegram.ext as ext

def main(dispatcher):
    get_word_handler = ext.CommandHandler('get_word', get_word)
    dispatcher.add_handler(get_word_handler)

def get_word(bot, update):
    word = words.get_daily_word()

    update.message.reply_text('%s - %s' % (word['word'], word['meaning']))
