# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

import connectors.words as words
import telegram
import telegram.ext as ext
import utils.word_utils as word_utils

def main(dispatcher):
    suggest_handler = ext.CommandHandler('suggest', __suggest)
    dispatcher.add_handler(suggest_handler)

def __suggest(bot, update):
    suggested_word = update.message.text.replace('/suggest', '').strip()

    message_text = ''

    if suggested_word:
        try:
            suggestion_id = word_utils.insert_suggestion(
                                suggested_word,
                                update.message.from_user.id,
                                update.message.from_user.username)
            
            message_text = ('Your suggestion has been successfully added.\n\n' 
                            'The operation id is `{}` (just a reference in '
                            'case you need it, not really important).').format(suggestion_id)
        except Exception:
            message_text = ('There was an error inserting your suggestion.'
                            'If the problem persists, please contact @alesanmed.')
    else:
        message_text = "You didn't send any word. Please suggest a word."
    
    update.message.reply_markdown(message_text)