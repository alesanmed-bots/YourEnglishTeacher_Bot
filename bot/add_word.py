# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

import copy
import connectors
import telegram
import telegram.ext as ext
import requests
import logging
import os
from connectors import oxford_api

WORD, MEANING, MEANING_ERROR = range(3)
_MEANING_ERROR_COUNTER_ = 0
_NEW_WORD_ = None

def main(dispatcher):
    add_word_handler = ext.ConversationHandler(
        entry_points=[ext.CommandHandler('add_word', __add_word)],

        states={
            WORD: [ext.MessageHandler(ext.Filters.text, __set_word)],
            MEANING: [ext.MessageHandler(ext.Filters.text, __set_meaning),
                      ext.CallbackQueryHandler(__word_meaning_verification, pattern=r'^word_meaning:\d$')
                    ],
            MEANING_ERROR: [ext.MessageHandler(ext.Filters.text, __handle_meaning_error)],
        },

        fallbacks=[ext.CommandHandler('cancel', __add_word_cancel)]
    )
    
    dispatcher.add_handler(add_word_handler)
    
def __add_word(bot, update):
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

def __set_word(bot, update):
    global _NEW_WORD_

    _NEW_WORD_['word'] = update.message.text

    next_state = MEANING

    if connectors.words.check_duplicate_word(_NEW_WORD_['word']):
        update.message.reply_text("Thank you for sending me a word, but I already have that word stored. Send me another one or /cancel, please")

        next_state = WORD
    else:
        meaning_request = oxford_api.get_word_definition(_NEW_WORD_['word'])

        if meaning_request.status_code == 200:
            meaning_json = meaning_request.json()

            __process_word(meaning_json)

            message_text = 'Please, review the word meaning:\n'

            for i, meaning in enumerate(_NEW_WORD_['meanings']):
                line = '%s. (%s) %s\n\n' % (i+1, meaning['category'], meaning['definition'])

                message_text += line
            
            message_text += '\nIs this correct?'

            update.message.reply_text(message_text, reply_markup=__get_reply_keyboard())
        else:
            _NEW_WORD_['pronunciation'] = None
            update.message.reply_text(
                "Well, I'm having troubles retrieving the word meaning... " +
                "please send me the word definition (in english, please)")

    return next_state

def __word_meaning_verification(bot, update):
    global _NEW_WORD_

    next_state = ext.ConversationHandler.END

    callback = update.callback_query
    callback_data = update.callback_query.data

    definition_ok = int(callback_data.split(':')[-1])

    callback.answer()
    callback.edit_message_reply_markup()
    
    if definition_ok:
        connectors.words.insert_word(_NEW_WORD_)

        _NEW_WORD_ = None

        callback.message.reply_text("Perfect, your word has been added!")
        next_state = ext.ConversationHandler.END
    else:
        callback.message.reply_text("Well, in that case please send me the word meaning in english")
        next_state = MEANING
    
    return next_state

def __set_meaning(bot, update):
    global _NEW_WORD_

    next_state = ext.ConversationHandler.END

    word_meaning = update.message.text

    _NEW_WORD_['from'] = 'manual_input'

    if word_meaning:
        _NEW_WORD_['meanings'] = [{
            'category': None,
            'definition': word_meaning,
            'example': None
            }]

        connectors.words.insert_word(_NEW_WORD_)

        _NEW_WORD_ = None

        update.message.reply_text("Perfect, your word has been added!")
    else:
        next_state = MEANING_ERROR

    return next_state

def __handle_meaning_error(bot, update):
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


def __add_word_cancel(bot, update):
    global _NEW_WORD_

    _NEW_WORD_ = None

    update.message.reply_text("Ok, no word will be added")

    return ext.ConversationHandler.END

def __get_reply_keyboard():
    keyboard = [
        [telegram.InlineKeyboardButton('That\'s correct', callback_data='word_meaning:1')], 
        [telegram.InlineKeyboardButton('No, it\'s not correct', callback_data='word_meaning:0')]
    ]

    return telegram.InlineKeyboardMarkup(keyboard)

def __process_word(word_json):
    lexical_entries = word_json['results'][0]['lexicalEntries']

    meanings = []

    for lexical_entry in lexical_entries:
        meaning = {
            'category': lexical_entry['lexicalCategory']
        }

        if 'pronunciation' not in _NEW_WORD_:
            _NEW_WORD_['pronunciation'] = lexical_entry['pronunciations'][0]['phoneticSpelling']

            __save_audio_file(lexical_entries)

        for sense in lexical_entry['entries'][0]['senses']:
            meaning['definition'] = sense['definitions'][0]

            if 'examples' in sense:
                meaning['example'] = sense['examples'][0]['text']
            else:
                meaning['example'] = None

            meanings.append(copy.deepcopy(meaning))

            meaning.pop('definition', None)
            meaning.pop('example', None)

    _NEW_WORD_['meanings'] = meanings

    _NEW_WORD_['from'] = 'oxford'

    return True
            
def __save_audio_file(lexical_entries):
    global _NEW_WORD_

    for lexical_entry in lexical_entries:
        for pronunciation in lexical_entry['pronunciations']:
            if 'audioFile' in pronunciation:
                audio_file_raw = requests.get(pronunciation['audioFile'])

                try:
                    audio_file_raw.raise_for_status()
                except:
                    logging.getLogger().info(
                        'Audio could not be downloaded. URL: %s, Status: %s' % 
                        (pronunciation['audioFile'], audio_file_raw.status_code))
                    return False
                
                audio_file = open(
                    os.path.normpath(os.path.join(
                        os.path.dirname(os.path.realpath(__file__)), 
                        '../assets/audio_files/', 
                        '%s.mp3' % (_NEW_WORD_['word'].lower(),)
                    )), 'wb')

                for chunk in audio_file_raw.iter_content(100000):
                    audio_file.write(chunk)
                audio_file.close()
                
            return True