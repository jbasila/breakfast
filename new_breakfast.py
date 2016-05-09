#!/usr/bin/env python

from telegram import Emoji, ForceReply, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import argparse, ConfigParser

class EtaChat(object):
    token = None
    chat_id = None
    timeout = None
    custom_keyboard = None
    reply_markup = None

    def __init__(self, token, chat_id, timeout):
        self.token = token
        self.chat_id = chat_id
        self.timeout = timeout
        self.updater = Updater(self.token)
        self.custom_keyboard = [['Here', '7:30', '8:00'], ['8:30', '9:00', '9:30'], ['Won\'t make it']]
        self.reply_markup = ReplyKeyboardMarkup(self.custom_keyboard, one_time_keyboard=True)
        self.updater.dispatcher.addHandler(MessageHandler([Filters.text], self.set_value))

    def start_eta_collection(self):
        self.updater.bot.sendMessage(self.chat_id,
                                     text="ETA?",
                                     reply_markup=self.reply_markup)

    def run(self):
        def beep(bot):
            self.start_eta_collection()

        self.updater.job_queue.put(beep, self.timeout, repeat=False)
        # Start the Bot
        self.updater.start_polling()

        # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT
        self.updater.idle()

    def set_value(self, bot, update):
        print update


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf",
                        help="Configuration file")
    args = parser.parse_args()

    # cfg = ConfigParser()
    # cfg.read(args.conf)

    eta_chat = EtaChat('204898432:AAHVAeO_XdF3i5hdty_88GFq_2DxmSotPAo',
                       '105584280',
                       5)

    eta_chat.run()


if __name__ == '__main__':
    main()
