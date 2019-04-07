# -*- coding: utf-8 -*-
import sys
import time
import logging
import telegram
import pymeteoapi
import datetime, time

from pid import PidFile
from configparser import SafeConfigParser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

timeformat = '%Y-%m-%d %H:%M:%S'


BOT_TOKEN = ""
circuitbreaker_status = True
enabled_scheduler = True
masters_inda_haus = {}

def telegram_start(bot, update):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    location_keyboard = telegram.KeyboardButton(text="Enviar posició", request_location=True)
    custom_keyboard = [[ location_keyboard ]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=chat_id,
                     text="Si us plau, comparteix la teva ubicació per buscar la platja més propera",
                     reply_markup=reply_markup)

def location(bot, update):
    update.message.reply_text("loc: "+str(update.message.location), use_aliases=True)
    platges_candidates = pymeteoapi.llista_platjes(update.message.location['latitude'], update.message.location['longitude'])
    logging.info(str(platges_candidates))

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
        dbfile = config.get('bot', 'db-file').strip('"').strip("'").strip()

        try:
            pymeteoapi.setup(user=config.get('meteoapi', 'user').strip('"').strip("'").strip(),password=config.get('meteoapi', 'password').strip('"').strip("'").strip(),db=config.get('meteoapi', 'db').strip('"').strip("'").strip())
        except:
            logging.error("unable to parse meteoapi options")
            sys.exit(1)

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
        updater.dispatcher.add_handler(MessageHandler(Filters.location, location))

        updater.start_polling()

        updater.idle()
