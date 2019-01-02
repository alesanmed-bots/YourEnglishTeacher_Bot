# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

import connectors
import telegram
import telegram.ext as ext
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from connectors import words

def main(dispatcher):
    get_suggestions_handler = ext.CommandHandler('get_suggestions', __get_suggestions)

    get_suggestions_callback_handler = ext.CallbackQueryHandler(__handle_suggestion_callback, pattern=r'^[1,0],.*$')
    
    dispatcher.add_handler(get_suggestions_handler)
    dispatcher.add_handler(get_suggestions_callback_handler)

def __get_suggestions(bot, update):
    if connectors.authentication.check_authorization(
            update.message.from_user.id):
        suggestions = words.get_suggestions()

        message = ''

        for suggestion in suggestions:
            if suggestion['status'] == None:
                if message:
                    update.message.reply_text(message)
                
                message = '{}\n\nProposed by {} ({}) on {}'.format(
                    suggestion['suggestion'],
                    suggestion['user_id'],
                    suggestion['username'],
                    suggestion['added'].strftime('%d-%m-%Y %H:%M'))
                
                update.message.reply_text(message, reply_markup=__get_keyboard(suggestion['_id']))

                message = ''
            else:
                message += __get_status_text(suggestion)


def __handle_suggestion_callback(bot, update):
    callback_query = update.callback_query

    callback_data = callback_query.data.split(',')

    new_status = int(callback_data[0])

    suggestion_id = callback_data[1]

    updated_suggestion = words.update_suggestion(suggestion_id, new_status)

    callback_query.edit_message_text(text=__get_status_text(updated_suggestion))

def __get_keyboard(suggestion_id):
    keyboardMarkup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(
            '✅ Accept',
            callback_data='1,{}'.format(suggestion_id)), 
          InlineKeyboardButton(
            '❌ Reject', 
            callback_data='0,{}'.format(suggestion_id))]]
    )

    return keyboardMarkup

def __get_status_text(suggestion):
    emoji = ''
    status = ''

    if int(suggestion['status']) == 1:
        emoji = '✅'
        status = 'Accepted'
    else:
        emoji = '❌'
        status = 'Rejected'

    text = '{} {}. Proposed by {} ({}). {} on {}\n'.format(
        emoji,
        suggestion['suggestion'],
        suggestion['user_id'],
        suggestion['username'],
        status,
        suggestion['last_update'].strftime('%d-%m-%Y')
    )

    return text