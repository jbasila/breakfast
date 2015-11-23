import telegram


TOKEN = ''
CHAT_ID = 0


def smack_these_etas(bot):
    """
    :type bot: telegram.Bot

    """
    bot.sendMessage(chat_id=CHAT_ID, text='ETAs')
    bot.sendMessage(chat_id=CHAT_ID, text='john: 7:25')
    bot.sendMessage(chat_id=CHAT_ID, text='sagi: 8:08')
    bot.sendMessage(chat_id=CHAT_ID, text='noam: >=10')
    bot.sendMessage(chat_id=CHAT_ID, text='yoav: wait for me guys!')
    bot.sendSticker(chat_id=CHAT_ID, sticker='BQADAwADNQADYK6GBTswjvGbLJgxAg')
    bot.sendMessage(chat_id=CHAT_ID, text='noam: john, gila tomorrow?')
    bot.sendMessage(chat_id=CHAT_ID, text='sagi:')
    bot.sendSticker(chat_id=CHAT_ID, sticker='BQADBAADcgADD4KaAAEfqtBiFqveBQI')


def main():
    bot = telegram.Bot(token=TOKEN)
    smack_these_etas(bot)


if __name__ == '__main__':
    main()
