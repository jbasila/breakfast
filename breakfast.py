from ConfigParser import ConfigParser

import telegram
import time


class Breakfast(object):
    token = None
    chat_id = None
    timeout = None

    def __init__(self, conf_fname):
        self.load_conf(conf_fname)
        self.bot = telegram.Bot(token=self.token)

    def load_conf(self, fname):
        cfg = ConfigParser()
        cfg.read(fname)
        self.token = cfg.get('global', 'token')
        self.chat_id = cfg.getint('global', 'chat_id')
        self.timeout = cfg.getint('global', 'timeout')  # in seconds

    def smack_these_etas(self):
        self.bot.sendMessage(chat_id=self.chat_id, text='ETAs')
        self.bot.sendMessage(chat_id=self.chat_id, text='john: 7:25')
        self.bot.sendMessage(chat_id=self.chat_id, text='sagi: 8:08')
        self.bot.sendMessage(chat_id=self.chat_id, text='noam: >=10')
        self.bot.sendMessage(chat_id=self.chat_id, text='yoav: wait for me guys!')
        self.bot.sendSticker(chat_id=self.chat_id, sticker='BQADAwADNQADYK6GBTswjvGbLJgxAg')
        self.bot.sendMessage(chat_id=self.chat_id, text='noam: john, gila tomorrow?')
        self.bot.sendMessage(chat_id=self.chat_id, text='sagi:')
        self.bot.sendSticker(chat_id=self.chat_id, sticker='BQADBAADcgADD4KaAAEfqtBiFqveBQI')

    def normal_day(self):
        here_msgs = ['here!', '7:25', '8:08']
        loser_msgs = ["I'm a loser!"]
        here = set()
        losers = set()

        self.clean_srv_msgs()

        custom_keyboard = [here_msgs + ['>=10'] + loser_msgs]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        self.bot.sendMessage(chat_id=self.chat_id, text='ETAs?', reply_markup=reply_markup)

        time.sleep(self.timeout)
        updates = self.bot.getUpdates()

        for i in updates:
            if i.message.text in here_msgs:
                here.add(self.get_name(i.message.from_user))
            if i.message.text in loser_msgs:
                losers.add(self.get_name(i.message.from_user))

        if len(here) == 0:
            self.bot.sendSticker(chat_id=self.chat_id, sticker='BQADAwADegADv4yQBIEb_nJ9h1mRAg',
                                 reply_markup=telegram.ReplyKeyboardHide())
        elif len(here) == 1:
            self.bot.sendMessage(chat_id=self.chat_id, text='{}, may the force be with you'.format(list(here)[0]),
                                 reply_markup=telegram.ReplyKeyboardHide())
        else:
            self.bot.sendMessage(chat_id=self.chat_id, text='{} brogrammers gonna have fun'.format(len(here)),
                                 reply_markup=telegram.ReplyKeyboardHide())

        if len(losers) > 0:
            self.bot.sendMessage(chat_id=self.chat_id, text='It appears that {} {} low self esteem'.format(
                self.comma_names(losers), 'has' if len(losers) == 1 else 'have'))

    def clean_srv_msgs(self):
        updates = self.bot.getUpdates()
        while len(updates) > 0:
            updates = self.bot.getUpdates(updates[-1].update_id + 1)

    def get_name(self, chat):
        """
        :type chat: telegram.user.User
        :rtype: str

        """
        if chat.first_name:
            res = chat.first_name
        elif chat.last_name:
            res = chat.last_name
        elif chat.username:
            res = chat.username
        else:
            res = 'anonymous lady'
        return res

    @staticmethod
    def comma_names(names):
        names = list(names)
        x = len(names)
        if x == 0:
            res = ''
        elif x == 1:
            res = names[0]
        else:
            res = '{} and {}'.format(', '.join(names[:-1]), names[-1])
        return res


def main():
    breakfast = Breakfast('breakfast.conf')
    # breakfast.smack_these_etas()
    breakfast.normal_day()

if __name__ == '__main__':
    main()
