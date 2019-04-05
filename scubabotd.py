import sys
import time
import json
import logging
import schedule
import telegram
import datetime, time

from pid import PidFile
from ConfigParser import SafeConfigParser
from telegram.ext import Updater, CommandHandler

timeformat = '%Y-%m-%d %H:%M:%S'


BOT_TOKEN = ""
circuitbreaker_status = True
enabled_scheduler = True
masters_inda_haus = {}

def telegram_start(bot, update):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    update.message.reply_text("scubabot", use_aliases=True)

# main
if __name__ == "__main__":
    with PidFile('scubabotd') as pidfile:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        try:
            configfile = sys.argv[1]
        except IndexError:
            configfile = './scubabot.config'

        config = SafeConfigParser()
        config.read(configfile)

        BOT_TOKEN = config.get('bot', 'token').strip('"').strip("'").strip()

        try:
            debug = config.getboolean('bot', 'debug')
        except:
            debug = False


        #
        # telegram
        #

        updater = Updater(token=BOT_TOKEN)

        dp = updater.dispatcher

        updater.dispatcher.add_handler(CommandHandler('start', telegram_start))

        updater.start_polling()

        updater.idle()
