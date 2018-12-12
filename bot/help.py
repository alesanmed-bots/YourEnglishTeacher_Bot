# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

import connectors
from telegram.ext import CommandHandler

def main(dispatcher):
    help_handler = CommandHandler('help', __help)
    dispatcher.add_handler(help_handler)
    
def __help(bot, update):
    message = ('/start Registers you in the bot and make the bot '
                'send you a new word each day.\n'
                '/suggest [word] Suggests a word for being added to'
                ' the bot. The suggestions are revised by admins and'
                ' they decide if the word suggested is added or not.\n'
                '/about Shows a message with some info about the bot, '
                'the developer who created it and how to contact him.\n'
                '/help Shows a message with all the commands available for you.')

    if connectors.authentication.check_authorization(
            update.message.from_user.id):
        message += ('\n\n<b>-- Admin commands --</b>\n\n'
                    '/add_word Begins the conversation for adding a new word.\n'
                    '/auth [token] Authorizes you use private commands.\n'
                    '/get_suggestions Retrieves the word suggestions for managing them.\n'
                    '/send_broadcast Sends a broadcast message to all registered users.\n')

    update.message.reply_html(message)