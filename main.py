from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv

from settings import delay, elements_value, filename
from source.CsvUser import CsvUser
from source.SeleniumS import SeleniumS
from source.TelegramBot import TelegramBot


load_dotenv()
token = os.getenv("TOKEN")
id_channel = os.getenv("ID_CHANNEL")
link = os.getenv("LINK")


if __name__ == '__main__':
    tbot = TelegramBot(token)

    while True:
        selenium_bot = SeleniumS(headless=True)
        selenium_bot.get_page(link)
        selenium_bot.make_screenshot()
        attribute_list = selenium_bot.get_attributes_list(By.CLASS_NAME, elements_value, By.TAG_NAME, 'a', 'href')
        csv_user = CsvUser(filename)
        rows = csv_user.read_csv()
        for attribute in attribute_list:
            if [attribute] not in rows:
                csv_user.write_csv([attribute])
                print(attribute, '--', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                tbot.send_message(id_channel, text=attribute)
                time.sleep(5)
            else:
                print('строка уже существует', '--', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        selenium_bot.close()

        time.sleep(delay * 60)