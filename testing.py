#!/usr/bin/env python

from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from configparser import ConfigParser

def set_value(bot, update):
    print(update)


def main():
    custom_keyboard = [['A1', 'A2', 'A3'],
                       ['B1', 'B2', 'B3'],
                       ['C']]

    cfg = ConfigParser()
    cfg.read('bot.cfg')

    updater = Updater(cfg.get('bot', 'token_id'))
    chat_id = cfg.getint('bot', 'chat_id')

    reply_markup = ReplyKeyboardMarkup(custom_keyboard,
                                       one_time_keyboard=True)

    updater.dispatcher.add_handler(MessageHandler([Filters.text],
                                                  set_value))
    # self.updater.job_queue.put(beep, 0, repeat=False)
    # Start the Bot
    updater.start_polling()

    updater.bot.sendMessage(chat_id,
                            text="ETA?",
                            reply_markup=reply_markup)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
