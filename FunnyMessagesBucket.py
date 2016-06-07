
import random


class MessagesBucket(object):
    def __init__(self):
        pass

    @staticmethod
    def _chose_random_message(_messages_array):
        _choice = _messages_array[random.randint(0, len(_messages_array) - 1)]
        return _choice[0], _choice[1]

    def respect_previous_creators(self):
        _messages_array = [['text', 'I usually tend to ignore or blow others away but my master told me to be polite '
                                    'to you specifically Mr. Noam. So I will be polite and tell you that I have only '
                                    'one master and that is not you :). You have a great day now! I will be ignoring '
                                    'messages now.']]

        return self._chose_random_message(_messages_array)

    def not_collecting_eta(self):
        _messages_array = [['text', 'Not collecting ETA currently'],
                           ['text', 'Dude, did you just wake up or something, I\'m not collecting ETA anymore!'],
                           ['text', 'Good to know, thank you for sharing, but I\'m not collecting ETA dude!'],
                           ['text', 'Yeah, no'],
                           ['text', 'Check your watch dude, not collecting ETA anymore!'],
                           ['text', 'All lines are busy right now please hold the line and we will be with you tomorrow'
                                    ' - maybe!'],
                           ['text', 'Please direct your message to /dev/null and we will be with you shortly -- NOT :)'],
                           ['text', 'Please don\'t call us, we\'ll call you!'],
                           ['text', 'In which time zone are in exactly?']]

        return self._chose_random_message(_messages_array)

    def bot_is_now_online(self):
        _messages_array = [['text', 'Bot is now online'],
                           ['text', 'OK I\'m here, now what?'],
                           ['text', 'I\'m up I\'m up -- geez'],
                           ['text', 'Isn\'t this great - I\'m alive again'],
                           ['text', '(yawn) - morning!']]

        return self._chose_random_message(_messages_array)

    def ask_for_eta(self):
        _messages_array = [['text', 'ETA?'],
                           ['text', 'Hungry?'],
                           ['text', 'Wakey wakey!'],
                           ['text', 'Come on - start pressing the buttons:'],
                           ['text', 'Yow yow yow - push d\'button:']]

        return self._chose_random_message(_messages_array)

    def done_collecting_eta(self):
        _messages_array = [['text', 'Done for now, here is the status:'],
                           ['text', 'Ladies and gents we have a final conclusion:'],
                           ['text', 'Ok thank god it\'s over! results:'],
                           ['text', 'I\'m out of here:']]

        return self._chose_random_message(_messages_array)

    def no_double_votes(self):
        _messages_array = [['text', 'You already voted!'],
                           ['text', 'Changed your mind? it\'s your problem not mine!'],
                           ['text', 'Stop pressing the buttons - I heard you the first time!'],
                           ['text', 'Hay look, it\'s the double voter again!'],
                           ['text', 'Let\'s hear it for Mr. double vote!'],
                           ['text', 'Your double vote has been ignored successfully!'],
                           ['text', 'I\'m running out of funny messages, please stop!'],
                           ['sticker', 'BQADBAADGwADmBZLBgG6GBWnKoqGAg']]

        return self._chose_random_message(_messages_array)

    def invalid_eta_input(self):
        _messages_array = [['text', 'You would think if you create a keyboard with buttons, people would simply '
                                    'use it but no they are smarter, well you know what, your not!'],
                           ['text', 'Try the custom keyboard will ya!'],
                           ['text', 'Segmentation Fault!'],
                           ['text', 'I created a custom keyboard so you won\'t make a mistake - and you still made '
                                    'a mistake!']]

        return self._chose_random_message(_messages_array)
