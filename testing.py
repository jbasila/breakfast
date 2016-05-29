#!/usr/bin/env python

from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

def set_value(bot, update):
    print(update)


def main():
    custom_keyboard = [['A1', 'A2', 'A3'],
                       ['B1', 'B2', 'B3'],
                       ['C']]

    updater = Updater('204898432:AAGrfj82Lt8VxNW6oDXrEoamqe2Mk4byiMQ')
    chat_id = -141663891
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
