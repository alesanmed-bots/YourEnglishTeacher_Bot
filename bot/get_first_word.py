# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

import connectors.words as words
import telegram.ext as ext

def main(dispatcher):
    get_first_word_handler = ext.CommandHandler('get_first_word', get_first_word)
    dispatcher.add_handler(get_first_word_handler)

def get_first_word(bot, update):
    word = words.get_first_word()

    update.message.reply_text('%s - %s' % (word['word'], word['meaning']))
