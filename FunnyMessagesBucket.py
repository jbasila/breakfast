
import random


class MessagesBucket(object):
    def __init__(self):
        pass

    @staticmethod
    def _chose_random_message(messages_array):
        return messages_array[random.randint(0, len(messages_array) - 1)]

    @staticmethod
    def respect_previous_creators():
        _messages_array = ['I usually tend to ignore or blow others away but my '
                           'master told me to be polite to you specifically Mr. '
                           'Noam. So I will be polite and tell you that I have '
                           'only one master and that is not you :). You have a '
                           'great day now! I will be ignoring messages now.']

        return MessagesBucket._chose_random_message(_messages_array)

    @staticmethod
    def not_collecting_eta():
        _messages_array = ['Not collecting ETA currently',
                           'Dude, did you just wake up or something, I\'m not collecting ETA anymore!',
                           'Good to know, thank you for sharing, but I\'m not collecting ETA dude!',
                           'Yeah, no',
                           'Check your watch dude, not collecting ETA anymore!',
                           'All lines are busy right now please hold the line and we will be with you tomorrow '
                           '- maybe!',
                           'Please direct your message to /dev/null and we will be with you shortly -- NOT :)',
                           'Please don\'t call us, we\'ll call you!',
                           'In which time zone are in exactly?']

        return MessagesBucket._chose_random_message(_messages_array)

    @staticmethod
    def bot_is_now_online():
        _message_array = ['Bot is now online',
                          'OK I\'m here, now what?',
                          'I\'m up I\'m up -- geez',
                          'Isn\'t this great - I\'m alive again',
                          '(yawn) - morning!']

        return MessagesBucket._chose_random_message(_message_array)

    @staticmethod
    def no_double_votes():
        _messages_array = ['You already voted!',
                           'Changed your mind? it\'s your problem not mine!',
                           'Stop pressing the buttons - I heard you the first time!',
                           'Hay look, it\'s the double voter again!',
                           'Let\'s hear it for Mr. double vote!',
                           'Your double vote has been ignored successfully!',
                           'I\'m running out of funny messages, please stop!']

        return MessagesBucket._chose_random_message(_messages_array)

    @staticmethod
    def invalid_eta_input():
        _messages_array = ['You would think if you create a keyboard with buttons, people would simply use it,'
                           ' but no they are smarter, well you know what, your not!',
                           'Try the custom keyboard that was created man, please!',
                           'Segmentation Fault!',
                           'I created a custom keyboard so you won\'t make a mistake - and you still made a mistake!']

        return MessagesBucket._chose_random_message(_messages_array)

