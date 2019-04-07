# -*- coding: utf-8 -*-
import sys
import time
import logging
import telegram
import pymeteoapi
import datetime, time

from pid import PidFile
from configparser import SafeConfigParser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

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
    platges = pymeteoapi.llista_platjes(update.message.location['latitude'], update.message.location['longitude'])
    logging.info(str(platges))
    count_platges=len(platges)

    if count_platges>2:
        keyboard = []
        for platja in platges:
            keyboard.append([InlineKeyboardButton(platja['nom'], callback_data='platges*selecciona*'+platja['slug'])])

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Selecciona una platja:', reply_markup=reply_markup)
    elif count_platges == 1:
        # TODO SELECCIONA PLATJA DIRECTAMENT
        update.message.reply_text("ENCARA NO SHA IMPLEMENTAT")
    else:
        update.message.reply_text("No s'han trobat platges properes")

def selector_handler(bot, update):
    # bot.send_chat_action(chat_id=update.callback_query.message.chat_id, action=telegram.ChatAction.TYPING)
    query = update.callback_query
    user_id = query.from_user.id
    #logging.debug("Cognom DISPLAY: "+update.message.from_user.last_name)
    #display_name = update.message.from_user.first_name+" "+update.message.from_user.last_name
    display_name = query.from_user.first_name

    input_data=[]
    input_data=query.data.split('*')

    if len(input_data) != 3:
        logging.debug('error input data')
        return

    bot.edit_message_text(text=input_data[2], chat_id=query.message.chat_id, message_id=query.message.message_id)

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
        updater.dispatcher.add_handler(CallbackQueryHandler(selector_handler))

        updater.start_polling()

        updater.idle()
