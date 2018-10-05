# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

import connectors
import telegram.ext as ext

WORD, MEANING, MEANING_ERROR, LANGUAGE_ERROR = range(4)
_MEANING_ERROR_COUNTER_ = 0
_NEW_WORD_ = None

def main(dispatcher):
    add_word_handler = ext.ConversationHandler(
        entry_points=[ext.CommandHandler('add_word', add_word)],

        states={
            WORD: [ext.MessageHandler(ext.Filters.text, set_word)],
            MEANING: [ext.MessageHandler(ext.Filters.text, set_meaning)],
            MEANING_ERROR: [ext.MessageHandler(ext.Filters.text, handle_meaning_error)]
        },

        fallbacks=[ext.CommandHandler('cancel', add_word_cancel)]
    )
    dispatcher.add_handler(add_word_handler)
    
def add_word(bot, update):
    global _NEW_WORD_
    _NEW_WORD_ = {}

    next_state = ext.ConversationHandler.END

    if connectors.authentication.check_authorization(
            update.message.from_user.id):
        update.message.reply_text("Let's add a word. You can cancel the process at any moment by sending" + 
                              " /cancel.\n\nFirst, which word do you want to add?")
        next_state = WORD
    else:
        update.message.reply_text("Sorry but you don't have enough priviledges to add a word.")

    return next_state

def set_word(bot, update):
    global _NEW_WORD_

    _NEW_WORD_['word'] = update.message.text

    update.message.reply_text("Nice. Now... tell me what that word means in spanish, please.")

    return MEANING

def set_meaning(bot, update):
    global _NEW_WORD_

    next_state = ext.ConversationHandler.END

    word_meaning = update.message.text

    if word_meaning:
        _NEW_WORD_['meaning'] = word_meaning

        connectors.words.insert_word(_NEW_WORD_)

        _NEW_WORD_ = None

        update.message.reply_text("Perfect, your word has been added!")
    else:
        next_state = MEANING_ERROR

    return next_state

def handle_meaning_error(bot, update):
    global _MEANING_ERROR_COUNTER_
    next_state = None

    if _MEANING_ERROR_COUNTER_ >= 1:
        update.message.reply_text("You don't have sent me a meaning for the word, no word will be added.")
        next_state = ext.ConversationHandler.END
    else:
        _MEANING_ERROR_COUNTER_ += 1
        update.message.reply_text("You don't have sent me a meaning for the word, please send it to me")
        next_state = MEANING
    
    return next_state


def add_word_cancel(bot, update):
    global _NEW_WORD_

    _NEW_WORD_ = None

    update.message.reply_text("Ok, no word would be added")