#!/usr/bin/env python

from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import argparse
from configparser import ConfigParser
from datetime import datetime
from FunnyMessagesBucket import MessagesBucket

WILL_JOIN_OPTIONS = ['Here', '7:30', '8:00', '8:30', '9:00', '9:30']
WONT_MAKE_IT = ['Won\'t make it']


class EtaChat(object):
    token = None
    chat_id = None
    timeout = None
    custom_keyboard = None
    reply_markup = None

    def __init__(self,
                 token,
                 chat_id,
                 admin_chat_id,
                 start_time,
                 end_time,
                 active_days):
        self.token = token
        self.chat_id = chat_id
        self.admin_chat_id = admin_chat_id
        self.start_time = start_time.split(':')
        self.end_time = end_time.split(':')
        self.active_days = [int(n) for n in active_days.split(',')]

        self._startTimeInt = int(self.start_time[0]) * 60 + int(self.start_time[1])
        self._endTimeInt = int(self.end_time[0]) * 60 + int(self.end_time[1])

        self.funny_message_bucket = MessagesBucket()

        self.eta_collection_on = False
        _now = datetime.now()
        _nowTimeInt = int(_now.hour) * 60 + int(_now.minute)
        self.is_active_time_interval = False
        if self._startTimeInt <= _nowTimeInt <= self._endTimeInt:
            self.is_active_time_interval = True
            self.eta_collection_on = True

        self.eta_dict = dict()

        self.updater = Updater(self.token)

        self.custom_keyboard = [WILL_JOIN_OPTIONS[:1],
                                WILL_JOIN_OPTIONS[1:4],
                                WILL_JOIN_OPTIONS[4:],
                                WONT_MAKE_IT]
        self.reply_markup = ReplyKeyboardMarkup(self.custom_keyboard,
                                                one_time_keyboard=True)

        self.updater.dispatcher.add_handler(CommandHandler('start', self.command_start))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.command_help))
        self.updater.dispatcher.add_handler(CommandHandler('begin', self.command_begin))
        self.updater.dispatcher.add_handler(CommandHandler('send', self.command_send))
        self.updater.dispatcher.add_handler(CommandHandler('end', self.command_end))
        self.updater.dispatcher.add_handler(MessageHandler([Filters.text], self.message_received))
        self.updater.dispatcher.add_handler(MessageHandler([Filters.sticker, Filters.photo], self.sticker_received))

    @staticmethod
    def send_funny_message(bot, chat_id, message_func):
        message_type, message_content = message_func()
        if message_type == 'text':
            bot.send_message(chat_id,
                             text=message_content)
        elif message_type == 'sticker':
            bot.send_sticker(chat_id,
                             message_content)

    def do_begin_eta_collection(self):
        if not self.eta_collection_on:
            self.updater.bot.send_message(self.chat_id,
                                          text=self.funny_message_bucket.ask_for_eta()[1],
                                          reply_markup=self.reply_markup)
        self.eta_collection_on = True

    def do_end_eta_collection(self):
        if self.eta_collection_on:
            self.updater.bot.send_message(chat_id=self.chat_id,
                                          text=self.funny_message_bucket.done_collecting_eta()[1],
                                          reply_markup=ReplyKeyboardHide())
            # do the summary
            for key, value in self.eta_dict.iteritems():
                self.updater.bot.send_message(chat_id=self.chat_id,
                                              text='key = {}, value = {}'.format(key, value))

        self.eta_collection_on = False
        self.eta_dict.clear()

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
                _message_reply = self.funny_message_bucket.respect_previous_creators()[1]

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
        if update.message.chat_id == self.chat_id:
            if self.eta_collection_on:
                if update.message.from_user.id in self.eta_dict:
                    EtaChat.send_funny_message(self.updater.bot,
                                               self.chat_id,
                                               self.funny_message_bucket.no_double_votes)
                else:
                    # Sanity of input
                    if update.message.text in WILL_JOIN_OPTIONS or update.message.text in WONT_MAKE_IT:
                        self.eta_dict[update.message.from_user.id] = update.message.text
                    else:
                        EtaChat.send_funny_message(self.updater.bot,
                                                   self.chat_id,
                                                   self.funny_message_bucket.invalid_eta_input)
            else:
                EtaChat.send_funny_message(self.updater.bot,
                                           self.chat_id,
                                           self.funny_message_bucket.not_collecting_eta)

    def sticker_received(self, bot, update):
        print('STICKER: {}'.format(update))

    def run(self):
        def beep(bot):
            _now = datetime.now()
            _nowTimeInt = int(_now.hour) * 60 + int(_now.minute)

            if _now.isoweekday() not in self.active_days:
                # Not in the active day period
                return

            if self.is_active_time_interval:
                if self._startTimeInt <= _nowTimeInt <= self._endTimeInt:
                    pass
                else:
                    self.do_end_eta_collection()
                    self.is_active_time_interval = False
            else:
                if self._startTimeInt <= _nowTimeInt <= self._endTimeInt:
                    self.do_begin_eta_collection()
                    self.is_active_time_interval = True
                else:
                    pass

        self.updater.job_queue.put(beep, 1, repeat=True)
        # Start the Bot
        self.updater.start_polling()

        EtaChat.send_funny_message(self.updater.bot,
                                   self.chat_id,
                                   self.funny_message_bucket.bot_is_now_online)

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
                       cfg.get('breakfast', 'end_time'),
                       cfg.get('breakfast', 'active_days'))

    eta_chat.run()


if __name__ == '__main__':
    main()
