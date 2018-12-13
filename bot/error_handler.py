# encoding: utf-8
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

from connectors import users
from utils import logger

def main(dispatcher):
    dispatcher.add_error_handler(__error_handler)
    
def __error_handler(bot, update, error):
    logger.get_logger().error('ERROR RAISED: {}'.format(error))

    update.message.reply_text(
        ('Wow... It seems like there I\'m having '
        'troubles at this moment... Please, try '
        'again later and, if the problem persists, '
        'contact @alesanmed')
    )