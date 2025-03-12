from selenium import webdriver
from selenium.webdriver.common.by import By
import fake_useragent
import time
from settings import left_messages_class_name, right_messages_class_name, all_messages_class_name, send_message_field_class_name, send_message_button_class_name

class SeleniumS:
    def __init__(self, headless=False, use_fake_useragent=True):

        opts = webdriver.ChromeOptions()
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument("--disable-gpu")

        if headless:
            opts.add_argument('--headless') # запуск в фоновом режиме
            opts.add_argument('--no-sandbox')  # убирает ошибку запуска в headless режиме на сервере
        if use_fake_useragent:
            ua = fake_useragent.UserAgent(os=["Windows", "Chrome OS", "Mac OS X"]).random
            opts.add_argument(f"user-agent={ua}")

        self.driver = webdriver.Chrome(options=opts)
        self.driver.set_window_size(2560, 1600)

    def get_page(self, url):
        self.driver.implicitly_wait(20)
        self.driver.get(url)
        time.sleep(10)

    def make_screenshot(self):
        self.driver.save_screenshot(f'screenshots/screenshot'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'.png')

    def get_ads_links(self, elements_method_by, elements_value, element_method_by, element_value, attribute_name):
        attribute_list = []
        elements_list = self.driver.find_elements(elements_method_by, elements_value)
        for el in elements_list:
            attribute = el.find_element(element_method_by, element_value).get_attribute(attribute_name)
            if '?' in attribute:    # убираем лишние символы в ссылке
                attribute = attribute.split('?')[0]
            attribute_list.append(attribute)
        return attribute_list

    def get_message_history(self, **kwargs):
        try:
            # загружаем входящие и исходящие сообщения
            load_left_messages = self.driver.find_elements(By.CLASS_NAME, left_messages_class_name)
            load_right_messages = self.driver.find_elements(By.CLASS_NAME, right_messages_class_name)
            load_all_messages = self.driver.find_elements(By.CLASS_NAME, all_messages_class_name)
            left_messages_list = [message.text for message in load_left_messages]
            right_messages_list = [message.text for message in load_right_messages]
            all_messages_list = [message.text for message in load_all_messages]
            print('список сообщений от пользователя:', left_messages_list, '\nсписок всех сообщений: ', all_messages_list)


            messages_history_for_gpt = []
            for message in all_messages_list:
                if message in left_messages_list:
                    messages_history_for_gpt.append({"role": "user", "content": message.split('\n')[0]})
                elif message in right_messages_list:
                    messages_history_for_gpt.append({"role": "assistant", "content": message.split('\n')[0]})
            print('история диалога: ', messages_history_for_gpt)

            # загружаем последнее сообщение
            last_message = all_messages_list[-1]
            print('последнее сообщение: ', last_message)
            return last_message, messages_history_for_gpt

        except Exception as e:
            print('Ошибка чтения истории сообщений:', e)

    def send_message(self, message):
        send_message = self.driver.find_element(By.CLASS_NAME, send_message_field_class_name)
        send_message.send_keys(message)
        press_button = self.driver.find_element(By.CLASS_NAME, send_message_button_class_name)
        press_button.click()


    def close(self):
        self.driver.quit()


