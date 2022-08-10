import telebot

TOKEN = '5455554178:AAHD4PfHQ3WNZx0Tg-hssQxZXZfIGd2MwvM'
class Bot():

    bot = telebot.TeleBot(TOKEN)

    def polling(self):

        self.bot.polling(non_stop=True,interval=0)