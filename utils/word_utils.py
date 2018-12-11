# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

import os
import telegram
from utils import logger
from connectors import words

def __build_daily_message(word):
    message = '%s' % (word['word'],)

    if word['pronunciation']:
        message += ' (%s):\n' % (word['pronunciation'])
    else:
        message += ':\n'

    for i, meaning in enumerate(word['meanings']):
        line = '%s. ' % (i+1,)

        if meaning['category']:
            line += '(%s) ' % (meaning['category'])

        line += meaning['definition']

        if meaning['example']:
            line += '\n_%s_' % (meaning['example'],)
        
        line += '\n\n'

        message += line

    return message

def send_daily_word(word, chat_id, bot):
    bot.sendMessage(
            chat_id=chat_id,
            text=__build_daily_message(word),
            parse_mode=telegram.ParseMode.MARKDOWN)
    
    try:
        bot.send_voice(
            chat_id=chat_id,
            voice=open(os.path.normpath(os.path.join(
                        os.path.dirname(os.path.realpath(__file__)), 
                        '../assets/audio_files/', 
                        '%s.mp3' % (word['word'].lower(),)
                    )), 'rb'))
    except Exception as e:
        logger.get_logger().warning('Audio could not be sended, reason: %s' % (e,))

def insert_suggestion(suggestion, user_id, username):
    document = {
        'suggestion': suggestion,
        'user_id': user_id,
        'username': username or 'No name',
        'status': None
    }

    return words.insert_suggestion(document)