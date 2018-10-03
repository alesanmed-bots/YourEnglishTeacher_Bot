# encoding: utf-8
from telegram.ext import CommandHandler

def main(dispatcher):
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm YourEnglishTeacher. I will daily send to @TheChannel useful words so you can improve your english.")