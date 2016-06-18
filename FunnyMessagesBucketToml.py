import random
import toml
import argparse


class MessagesBucket(object):
    def __init__(self, conf_file):
        with open(conf_file) as config_file_handle:
            self.config = toml.loads(config_file_handle.read())

    @staticmethod
    def _chose_random_message(_messages_array):
        _choice = _messages_array[random.randint(0, len(_messages_array) - 1)]
        return _choice[0], _choice[1]

    def get_random_message(self, message_name):
        return self._chose_random_message(self.config['funny_messages'][message_name])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf",
                        help="toml Configuration file")
    args = parser.parse_args()
    funny_messages = MessagesBucket(args.conf)

    _test_array = ['respect_previous_creators',
                   'you_are_not_my_master',
                   'not_collecting_eta',
                   'bot_is_now_online',
                   'ask_for_eta',
                   'done_collecting_eta',
                   'only_one_answered',
                   'no_one_answered',
                   'wont_make_it_and_voted',
                   'you_can_not_vote',
                   'no_double_votes',
                   'invalid_eta_input']

    for _message_name in _test_array:
        print '{}: {}'.format(_message_name, funny_messages.get_random_message(_message_name))


if __name__ == '__main__':
    main()
