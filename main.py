import threading
from selenium.webdriver.common.by import By
import pickle
import time
import os
from dotenv import load_dotenv

from settings import delay, elements_value, elements_value_a_class, filename, prompt, main_page, auth_link
from source.CsvUser import CsvUser
from source.SeleniumS import SeleniumS
from source.TelegramBot import TelegramBot
from source.BS import BS
from source.AI import Gpt

load_dotenv()
token = os.getenv("TOKEN")
id_channel = os.getenv("ID_CHANNEL")
link = os.getenv("LINK")
base_url = os.getenv("AI_BASE_URL")
api_key = os.getenv("AI_API_KEY")
login = os.getenv("AVITO_LOGIN")
password = os.getenv("AVITO_PASSWORD")

prompt = prompt


def main(selenium=False):
    if selenium:
        selenium_bot = SeleniumS(headless=False)
        selenium_bot.get_page(link)
        selenium_bot.make_screenshot()
        attribute_list = selenium_bot.get_ads_links(By.CLASS_NAME, elements_value, By.TAG_NAME, 'a', 'href')
        selenium_bot.close()
    else:
        bs = BS(link)
        attribute_list = bs.get_links(elements_value, elements_value_a_class)

    csv_user = CsvUser(filename)
    rows = csv_user.read_csv()
    for attribute in attribute_list:
        if [attribute] not in rows:
            csv_user.write_csv([attribute])
            print(attribute, '--', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            tbot.send_message(id_channel, text=attribute, button=True)
            time.sleep(5)
        else:
            print('строка уже существует', '--', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


if __name__ == '__main__':

    def scraper_loop():
        while True:
            print('start scrub')
            main(selenium=False)  # Убедитесь, что main корректно обрабатывает selenium=False
            time.sleep(delay * 60)

    # Создаем экземпляр бота
    tbot = TelegramBot(token)

    # Запускаем потоки
    bot_thread = threading.Thread(target=tbot.run, daemon=True)
    bot_thread1 = threading.Thread(target=tbot.check_new_messages, daemon=True)  # Исправлено: передаем метод как объект
    scraper_thread = threading.Thread(target=scraper_loop, daemon=True)

    bot_thread.start()
    bot_thread1.start()
    scraper_thread.start()

    while True:
        time.sleep(1)