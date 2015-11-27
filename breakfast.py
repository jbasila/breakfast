import signal
import time
from ConfigParser import ConfigParser
from collections import Counter

import telegram

RELEASE_KEYBOARD = telegram.ReplyKeyboardHide()
HERE_MSGS = ['here!', '7:25', '8:08']
LOSER_MSGS = ["I'm a loser!"]


class Breakfast(object):
    token = None
    chat_id = None
    timeout = None

    def __init__(self, conf_fname):
        self.load_conf(conf_fname)
        self.bot = telegram.Bot(token=self.token)
        self.timed_out = 0

    def load_conf(self, fname):
        cfg = ConfigParser()
        cfg.read(fname)
        self.token = cfg.get('global', 'token')
        self.chat_id = cfg.getint('global', 'chat_id')
        self.timeout = cfg.getint('global', 'timeout')  # in seconds

    def send_msg(self, text, reply_markup=None):
        kwargs = dict(chat_id=self.chat_id, text=text)
        if reply_markup:
            kwargs['reply_markup'] = reply_markup
        return self.bot.sendMessage(**kwargs)

    def send_sticker(self, id_, reply_markup=None):
        kwargs = dict(chat_id=self.chat_id, sticker=id_)
        if reply_markup:
            kwargs['reply_markup'] = reply_markup
        return self.bot.sendSticker(**kwargs)

    def send_photo(self, id_, reply_markup=None):
        kwargs = dict(chat_id=self.chat_id, photo=id_)
        if reply_markup:
            kwargs['reply_markup'] = reply_markup
        return self.bot.sendPhoto(**kwargs)

    def smack_these_etas(self):
        self.send_msg('ETAs')
        self.send_msg('john: 7:25')
        self.send_msg('sagi: 8:08')
        self.send_msg('noam: >=10')
        self.send_msg('yoav: wait for me guys!')
        self.send_sticker('BQADAwADNQADYK6GBTswjvGbLJgxAg')
        self.send_msg('noam: john, gila tomorrow?')
        self.send_msg('sagi:')
        self.send_sticker('BQADBAADcgADD4KaAAEfqtBiFqveBQI')

    def gila_day(self):
        pass

    def normal_day(self):
        here = set()
        losers = set()
        repliers = Counter()
        custom_keyboard = [HERE_MSGS[:2], HERE_MSGS[2:] + ['>=10'], LOSER_MSGS]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
        last_upd = -1

        def send_summary(_signum, _frame):
            self.handle_normal_day_replies(last_upd, here, losers, repliers)
            if len(here) == 0:
                self.send_sticker('BQADAwADegADv4yQBIEb_nJ9h1mRAg', reply_markup=RELEASE_KEYBOARD)  # crying blond
                self.send_msg('no one is coming!!! :-(')
            elif len(here) == 1:
                self.send_msg('{}, you\'re eating alone. May the force be with you'.format(list(here)[0]),
                              reply_markup=RELEASE_KEYBOARD)
                self.send_sticker('BQADAQADKwEAAtpxZgcxjbgZ2PsfdwI')  # luke skywalker - stand on one hand
            else:
                self.send_msg('{} brogrammers gonna have fun'.format(len(here)), reply_markup=RELEASE_KEYBOARD)

            if len(losers) > 0:
                self.send_msg('It appears that {} {} low self esteem'.format(self.comma_names(losers),
                                                                             'has' if len(losers) == 1 else 'have'))
                self.send_sticker('BQADBAADjAADD4KaAAFQZH8V3rLRwAI')  # spiderman - look at him and laugh

            self.timed_out = 1

        self.clean_srv_msgs()
        self.send_msg('ETAs?', reply_markup)
        signal.signal(signal.SIGALRM, send_summary)
        signal.alarm(self.timeout)
        while not self.timed_out:
            last_upd = self.handle_normal_day_replies(last_upd, here, losers, repliers)
            time.sleep(5)

    def clean_srv_msgs(self):
        updates = self.bot.getUpdates()
        while updates:
            updates = self.bot.getUpdates(updates[-1].update_id + 1)

    def handle_normal_day_replies(self, last_upd, here, losers, repliers):
        """
        :type last_upd: int
        :type here: set
        :type losers: set
        :type repliers: Counter
        :rtype: int

        """
        updates = self.bot.getUpdates(last_upd + 1)
        if updates:
            for i in updates:
                fromu = i.message.from_user
                name = self.get_name(fromu)
                repliers[fromu.id] += 1
                if repliers[fromu.id] > 1:
                    if repliers[fromu.id] == 2:
                        self.send_msg('{}, double votes are only allowed in the knesset!'.format(name))
                        self.send_photo('AgADBAAD5qgxG1fLIwIDIV9LHsml3CwIcTAABHQ2QwuJWr9sheMBAAEC')  # oren hazan
                    continue
                if i.message.text in HERE_MSGS:
                    here.add(name)
                elif i.message.text in LOSER_MSGS:
                    losers.add(name)
            last_upd = updates[-1].update_id
        return last_upd

    @staticmethod
    def get_name(chat):
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
