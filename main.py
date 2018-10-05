#coding: utf-8
import signal
import sys
import os

from telegram.ext import Updater
from importlib import import_module
import inflection

import utils.logger as logger
import utils.periodic_job as periodic_job
import configurations.bot_config as bot_config
from commands import commands

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

updater = None

def load_commands(dispatcher):
    base_path = os.path.join(os.path.dirname(__file__), 'bot')
    files = os.listdir(base_path)

    for file_name in files:
        command, _ = os.path.splitext(file_name)

        module = import_module(f'.{command}', 'bot')

        module.main(dispatcher)
        

def graceful_exit(signum, frame):
    if(updater is not None):
        updater.bot.delete_webhook()
    
    sys.exit(1)

if __name__ == "__main__":
    logger.init_logger(f'logs/{bot_config.NAME}.log')

    updater = Updater(token=bot_config.TOKEN)

    dispatcher = updater.dispatcher

    load_commands(dispatcher)

    scheduler = BackgroundScheduler()

    trigger = CronTrigger(year='*', month='*', day='*', hour='*', minute='*', second='*/30')

    scheduler.add_job(periodic_job.send_daily_message, trigger=trigger, args=(updater.bot,))

    scheduler.start()
    
    if(bot_config.WEBHOOK):
        signal.signal(signal.SIGINT, graceful_exit)
        updater.start_webhook(listen=bot_config.IP, port=bot_config.PORT, url_path=bot_config.URL_PATH)
        updater.bot.set_webhook(url=bot_config.WEBHOOK_URL)
    else:
        updater.start_polling()