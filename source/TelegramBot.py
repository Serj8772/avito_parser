import telebot
from telebot import types
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv
from source.SeleniumS import SeleniumS
from source.AI import Gpt
from settings import prompt, main_page, auth_link, write_message_button, first_message, end_messages, send_message_field_class_name, send_message_button_class_name

load_dotenv()
login = os.getenv("AVITO_LOGIN")
password = os.getenv("AVITO_PASSWORD")
base_url = os.getenv("AI_BASE_URL")
api_key = os.getenv("AI_API_KEY")
id_channel = os.getenv("ID_CHANNEL")


class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.link_to_start_conversation = None

        # логинимся и обрабатываем новые сообщения Авито
        try:
            self.selenium_bot = SeleniumS(headless=False)
            self.selenium_bot.login(main_page, auth_link, login, password)

            # while True:
            #     self.selenium_bot.get_page('https://www.avito.ru/profile/messenger?unread=true')
            #     unread_messages = self.selenium_bot.get_unread_message(By.CLASS_NAME, 'router-link-root-sGqou')
            #     if unread_messages:
            #
            #         history = self.selenium_bot.get_message_history()
            #         if history is False:
            #             self.selenium_bot.get_page('https://www.avito.ru/profile/messenger?unread=true')
            #         elif history:
            #             gpt = Gpt(base_url, api_key, prompt)
            #             gpt_response = gpt.response(history)
            #             print('отправил историю в gpt')
            #             print(gpt_response)
            #             self.selenium_bot.send_message(gpt_response, send_message_field_class_name=send_message_field_class_name, send_message_button_class_name=send_message_button_class_name)
            #             time.sleep(3)
            #             self.selenium_bot.get_page('https://www.avito.ru/profile/messenger?unread=true')
            #         else:
            #             print('ошибка получения истории сообщений')
            #     else:
            #         print('нет новых сообщений')
            #         time.sleep(121)

        except Exception as e:
            print('ошибка обработки новых сообщений Авито', e)

    def check_new_messages(self):
        while True:
            self.selenium_bot.switch_to_first_tab()
            self.selenium_bot.get_page('https://www.avito.ru/profile/messenger?unread=true')
            unread_messages = self.selenium_bot.get_unread_message(By.CLASS_NAME, 'router-link-root-sGqou')
            if unread_messages:

                history = self.selenium_bot.get_message_history()
                if history is False:
                    self.selenium_bot.get_page('https://www.avito.ru/profile/messenger?unread=true')
                elif history:
                    gpt = Gpt(base_url, api_key, prompt)
                    gpt_response = gpt.response(history)
                    print('отправил историю в gpt')
                    print(gpt_response)
                    self.selenium_bot.send_message(gpt_response,
                                                   send_message_field_class_name=send_message_field_class_name,
                                                   send_message_button_class_name=send_message_button_class_name)
                    time.sleep(3)
                    self.selenium_bot.get_page('https://www.avito.ru/profile/messenger?unread=true')
                else:
                    print('ошибка получения истории сообщений')
            else:
                print('нет новых сообщений')
                time.sleep(121)

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
            self.send_first_message(self.link_to_start_conversation, id_channel)

    def run(self):
        try:
            print('bot polling...')
            self.register_handlers()
            self.bot.polling(non_stop=True)
        except Exception as e:
            print('ошибка при запуске бота', e)
            time.sleep(5)
            self.run()

    def send_first_message(self, link_to_start_conv, id_channel):
        try:

            self.selenium_bot.open_new_tab(link_to_start_conv)
            self.selenium_bot.click_on_button_write_message(By.XPATH, write_message_button)
            print('нажал кнопку "Написать сообщение"')


            history = self.selenium_bot.get_message_history()
            print('получил историю', history)
            if history is None:
                print('истории нет, отправляю первое сообщение')
                self.selenium_bot.send_message(first_message[0], send_message_field_class_name=send_message_field_class_name, send_message_button_class_name=send_message_button_class_name) # --------------- настроить рандом !!!
                time.sleep(5)
                close_message = f'первое сообщение для {link_to_start_conv} отправлено, закрываю вкладку'
                self.bot.send_message(id_channel, close_message)
                self.selenium_bot.close()



            # elif history is False:
            #     time.sleep(35)
            # elif any(end_message in history[-1]['content'].lower() for end_message in end_messages):
            #     self.selenium_bot.close()
            #     break
            # elif history:
            #     gpt = Gpt(base_url, api_key, prompt)
            #     gpt_response = gpt.response(history)
            #     print('отправил историю в gpt')
            #     print(gpt_response)
            #     self.selenium_bot.send_message(gpt_response, send_message_field_class_name=send_message_field_class_name, send_message_button_class_name=send_message_button_class_name)

            else:
                print('есть история')
                self.selenium_bot.close()

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.selenium_bot.close()


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