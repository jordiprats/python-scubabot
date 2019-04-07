# -*- coding: utf-8 -*-
import sys
import time
import sqlite3
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

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

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
