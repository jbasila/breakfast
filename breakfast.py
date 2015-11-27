from ConfigParser import ConfigParser
import telegram
import time

RELEASE_KEYBOARD = telegram.ReplyKeyboardHide()


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
        here_msgs = ['here!', '7:25', '8:08']
        loser_msgs = ["I'm a loser!"]
        here = set()
        losers = set()
        custom_keyboard = [here_msgs[:2], here_msgs[2:] + ['>=10'], loser_msgs]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

        self.clean_srv_msgs()
        self.send_msg('ETAs?', reply_markup)
        time.sleep(self.timeout)
        updates = self.bot.getUpdates()

        for i in updates:
            if i.message.text in here_msgs:
                here.add(self.get_name(i.message.from_user))
            if i.message.text in loser_msgs:
                losers.add(self.get_name(i.message.from_user))

        if len(here) == 0:
            self.send_sticker('BQADAwADegADv4yQBIEb_nJ9h1mRAg', reply_markup=RELEASE_KEYBOARD)  # crying blond
            self.send_msg('no one is coming!!! :-(')
        elif len(here) == 1:
            self.send_msg('{}, may the force be with you'.format(list(here)[0]), reply_markup=RELEASE_KEYBOARD)
            self.send_sticker('BQADAQADKwEAAtpxZgcxjbgZ2PsfdwI')  # luke skywalker - stand on one hand
        else:
            self.send_msg('{} brogrammers gonna have fun'.format(len(here)), reply_markup=RELEASE_KEYBOARD)

        if len(losers) > 0:
            self.send_msg('It appears that {} {} low self esteem'.format(self.comma_names(losers),
                                                                         'has' if len(losers) == 1 else 'have'))
            self.send_sticker('BQADBAADjAADD4KaAAFQZH8V3rLRwAI')  # spiderman - look and him and laugh

    def clean_srv_msgs(self):
        updates = self.bot.getUpdates()
        while len(updates) > 0:
            updates = self.bot.getUpdates(updates[-1].update_id + 1)

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
