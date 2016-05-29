#!/usr/bin/env python

from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import argparse
from configparser import ConfigParser


class EtaChat(object):
    token = None
    chat_id = None
    timeout = None
    custom_keyboard = None
    reply_markup = None

    def __init__(self, token, chat_id, admin_chat_id, start_time, end_time):
        self.token = token
        self.chat_id = chat_id
        self.admin_chat_id = admin_chat_id
        self.start_time = start_time
        self.end_time = end_time

        self.eta_collection_on = False

        self.updater = Updater(self.token)
        self.custom_keyboard = [['Here', '7:30', '8:00'],
                                ['8:30', '9:00', '9:30'],
                                ['Won\'t make it']]
        self.reply_markup = ReplyKeyboardMarkup(self.custom_keyboard,
                                                one_time_keyboard=True)

        self.updater.dispatcher.add_handler(CommandHandler('start', self.command_start))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.command_help))
        self.updater.dispatcher.add_handler(CommandHandler('begin', self.command_begin))
        self.updater.dispatcher.add_handler(CommandHandler('send', self.command_send))
        self.updater.dispatcher.add_handler(CommandHandler('end', self.command_end))
        self.updater.dispatcher.add_handler(MessageHandler([Filters.text], self.set_value))

    def do_begin_eta_collection(self):
        if not self.eta_collection_on:
            self.updater.bot.sendMessage(self.chat_id,
                                         text="ETA?",
                                         reply_markup=self.reply_markup)
        self.eta_collection_on = True

    def do_end_eta_collection(self):
        if self.eta_collection_on:
            self.updater.bot.sendMessage(chat_id=self.chat_id,
                                         text='Done for now, here is the status:',
                                         reply_markup=ReplyKeyboardHide())
        self.eta_collection_on = False

    def do_start(self, bot, update):
        self.do_help(update)

    def do_help(self, update):
        message = ''
        self.updater.bot.sendMessage()

    def command_start(self, bot, update):
        print(update.message.chat.id)
        print(update.message.chat)
        print(update.message)

    def command_help(self, bot, update):
        pass

    def command_begin(self, bot, update):
        if update.message.chat.id == self.admin_chat_id:
            self.do_begin_eta_collection()

    def command_send(self, bot, update):
        if update.message.chat.id == self.admin_chat_id:
            self.updater.bot.sendMessage(self.chat_id,
                                         text=update.message.text[5:])

    def command_end(self, bot, update):
        if update.message.chat.id == self.admin_chat_id:
            self.do_end_eta_collection()

    def set_value(self, bot, update):
        print(update)

    def run(self):
        def beep(bot):
            self.do_begin_eta_collection()

        # self.updater.job_queue.put(beep, 0, repeat=False)
        # Start the Bot
        self.updater.start_polling()

        # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT
        self.updater.idle()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf",
                        help="Configuration file")
    args = parser.parse_args()

    cfg = ConfigParser()
    cfg.read(args.conf)

    eta_chat = EtaChat(cfg.get('bot', 'token_id'),
                       cfg.getint('bot', 'chat_id'),
                       cfg.getint('bot', 'admin_chat_id'),
                       cfg.get('breakfast', 'start_time'),
                       cfg.get('breakfast', 'end_time'))

    eta_chat.run()


if __name__ == '__main__':
    main()
