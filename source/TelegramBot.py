import telebot
from telebot import types
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv
from source.SeleniumS import SeleniumS
from source.AI import Gpt
from settings import prompt, main_page, auth_link, write_message_button_xpath, first_message, end_messages

load_dotenv()
login = os.getenv("AVITO_LOGIN")
password = os.getenv("AVITO_PASSWORD")
base_url = os.getenv("AI_BASE_URL")
api_key = os.getenv("AI_API_KEY")


class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.link_to_start_conversation = None

    def send_message(self, id_channel, text, button=False):
        if button:
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton('написать владельцу', callback_data="button_pressed")
            keyboard.add(button)
            self.bot.send_message(id_channel, text, reply_markup=keyboard)  # ✅ Добавляем клавиатуру
        else:
            self.bot.send_message(id_channel, text)

    # Отслеживание нажатия кнопки
    def register_handlers(self):
        @self.bot.callback_query_handler(func=lambda call: call.data == "button_pressed")
        def handle_button_press(call):
            self.link_to_start_conversation = call.message.text
            print(f"Кнопка нажата под сообщением: {self.link_to_start_conversation}")

            self.bot.answer_callback_query(call.id, "Вы нажали кнопку!")
            self.bot.send_message(call.message.chat.id, "Передаю ссылку для начала диалога")
            self.ai_messenger(self.link_to_start_conversation)

    def run(self):
            print('bot polling...')
            self.register_handlers()
            self.bot.polling(non_stop=True)

    def ai_messenger(self, link_to_start_conv):
        try:
            selenium_bot = SeleniumS(headless=False)
            selenium_bot.login(main_page, auth_link, login, password)

            selenium_bot.get_page(link_to_start_conv)
            selenium_bot.click_on_button_write_message(By.XPATH, write_message_button_xpath)
            print('нажал кнопку "Написать сообщение"')

            while True:
                history = selenium_bot.get_message_history()
                print('получил историю', history)
                if history is None:
                    print('истории нет, отправляю первое сообщение')
                    selenium_bot.send_message(first_message[0]) # --------------- настроить рандом !!!
                elif history is False:
                    time.sleep(35)
                elif any(end_message in history[-1]['content'].lower() for end_message in end_messages):
                    selenium_bot.close()
                    break
                elif history:
                    gpt = Gpt(base_url, api_key, prompt)
                    gpt_response = gpt.response(history)
                    print('отправил историю в gpt')
                    print(gpt_response)
                    selenium_bot.send_message(gpt_response)

                else:
                    print('ошибка получения истории сообщений')
                    break
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("TOKEN")
    id_channel = os.getenv("ID_CHANNEL")
    base_url = os.getenv("AI_BASE_URL")
    api_key = os.getenv("AI_API_KEY")

    bot = TelegramBot(token)
    text = "https://www.avito.ru/lobnya/kvartiry/2-k._kvartira_45_m_1518_et._7208849299"
    bot.send_message(id_channel, text, button=True)
    bot.run()