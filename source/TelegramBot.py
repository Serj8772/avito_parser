import telebot


class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def send_message(self, chat_id, text):
        self.bot.send_message(chat_id, text)