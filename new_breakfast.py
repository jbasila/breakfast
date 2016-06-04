#!/usr/bin/env python

from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import argparse
from configparser import ConfigParser
from datetime import datetime

WILL_JOIN_OPTIONS = ['Here', '7:30', '8:00', '8:30', '9:00', '9:30']

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
        self.start_time = start_time.split(':')
        self.end_time = end_time.split(':')

        self._startTimeInt = int(self.start_time[0]) * 60 + int(self.start_time[1])
        self._endTimeInt = int(self.end_time[0]) * 60 + int(self.end_time[1])

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
        self.updater.dispatcher.add_handler(MessageHandler([Filters.text], self.message_received))

    def do_begin_eta_collection(self):
        if not self.eta_collection_on:
            self.updater.bot.send_message(self.chat_id,
                                          text="ETA?",
                                          reply_markup=self.reply_markup)
        self.eta_collection_on = True

    def do_end_eta_collection(self):
        if self.eta_collection_on:
            self.updater.bot.send_message(chat_id=self.chat_id,
                                          text='Done for now, here is the status:',
                                          reply_markup=ReplyKeyboardHide())
        self.eta_collection_on = False

    def do_start(self, bot, update):
        self.do_help(update)

    def do_help(self, update):
        message = ''
        self.updater.bot.send_message()

    def command_start(self, bot, update):
        _message_reply = None
        if update.message.chat.id == self.admin_chat_id:
            _message_reply = 'Welcome master'
        else:
            # is this Noam?
            if update.message.chat.username == 'tsnoam':
                _message_reply = 'I usually tend to ignore or blow ' \
                                 'others away but my master told me to be polite ' \
                                 'to you specifically Mr. Noam. So I will be polite ' \
                                 'and tell you that I have only one master and that ' \
                                 'is not you :). You have a great day now! I will be ' \
                                 'ignoring messages now.'

            self.updater.bot.send_message(chat_id=self.admin_chat_id,
                                          text='Username ({} {} - @{}, chat_id = {}), '
                                               'tried to contact me'.format(update.message.chat.first_name,
                                                                            update.message.chat.last_name,
                                                                            update.message.chat.username,
                                                                            update.message.chat_id))

        if _message_reply is not None:
            self.updater.bot.send_message(chat_id=update.message.chat.id,
                                          text=_message_reply)

    def command_help(self, bot, update):
        pass

    def command_begin(self, bot, update):
        if update.message.chat.id == self.admin_chat_id:
            self.do_begin_eta_collection()

    def command_send(self, bot, update):
        if update.message.chat.id == self.admin_chat_id:
            self.updater.bot.send_message(self.chat_id,
                                          text=update.message.text[5:])

    def command_end(self, bot, update):
        if update.message.chat.id == self.admin_chat_id:
            self.do_end_eta_collection()

    def message_received(self, bot, update):
        # print(update.message)
        c = self.custom_keyboard.flatten()
        print(c)
        print(c)
        # if update.message.chat_id == self.chat_id:
        #     if self.eta_collection_on:
        #         pass

    def run(self):
        def beep(bot):
            _now = datetime.now()
            _nowTimeInt = int(_now.hour) * 60 + int(_now.minute)

            if _now.isoweekday() > 4:
                # Weekend, not doing notification
                return

            # Check if should start collecting time
            if self.eta_collection_on:
                # check if reached end of collection
                if self._startTimeInt <= _nowTimeInt <= self._endTimeInt:
                    # Still collecting
                    pass
                else:
                    # Reached end of collection, notify and let's do a summary.
                    self.do_end_eta_collection()
            else:
                # check if in time frame
                if self._startTimeInt <= _nowTimeInt <= self._endTimeInt:
                    self.do_begin_eta_collection()

        self.updater.job_queue.put(beep, 1, repeat=True)
        # Start the Bot
        self.updater.start_polling()

        self.updater.bot.send_message(self.admin_chat_id,
                                      text='Bot is now online')

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
