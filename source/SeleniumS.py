from selenium import webdriver

from selenium.webdriver.common.by import By
import fake_useragent
import time
import pickle
from settings import left_messages_class_name, right_messages_class_name, all_messages_class_name, send_message_field_class_name, send_message_button_class_name, main_page, auth_link, loggined_element_class_name

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

    def login(self, main_page, auth_link, login, password):
        try:
            # выгрузка и вход по cookies
            print('Выполняем вход по куки...')
            self.driver.get(main_page)
            time.sleep(10)
            self.driver.implicitly_wait(5)  # ожидание появление элемента в секундах
            cookies = pickle.load(open(f'{login}_cookies', 'rb'))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            time.sleep(5)
            self.driver.implicitly_wait(5)  # ожидание появление элемента в секундах

            self.driver.find_element(By.CLASS_NAME, loggined_element_class_name)

        except Exception as ex:
            print('Не удалось авторизоваться через куки', ex)

            try:
                # вход по логину паролю и загрузка cookies
                print('Авторизуемся по логину и паролю...')
                self.driver.get(auth_link)
                time.sleep(20)
                self.driver.implicitly_wait(5)  # ожидание появление элемента в секундах
                email_phone = self.driver.find_element(By.NAME, 'login')
                email_phone.send_keys(login)
                time.sleep(3)
                passwd = self.driver.find_element(By.NAME, 'password')
                passwd.send_keys(password)
                time.sleep(2)
                login_button = self.driver.find_element(By.NAME, 'submit')
                login_button.click()
                time.sleep(30)
                # сохраняем cookies
                pickle.dump(self.driver.get_cookies(), open(f'{login}_cookies', 'wb'))

                self.driver.find_element(By.CLASS_NAME, loggined_element_class_name)

            except Exception as ex:
                print('Не удалось авторизоваться через логин и пароль', ex)



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
            if len(all_messages_list) > 0:
                last_message = all_messages_list[-1]
                print('последнее сообщение: ', last_message)
                if last_message in left_messages_list:
                    return messages_history_for_gpt
                else:
                    return False
            else:
                return None
# остановился здесь!!!!!!!!!!!!

        except Exception as e:
            print('Ошибка чтения истории сообщений:', e)

    def click_on_button_write_message(self, button_method_by, button_value):
        button = self.driver.find_element(button_method_by, button_value)
        button.click()
        time.sleep(3)


    def send_message(self, message):
        send_message = self.driver.find_element(By.CLASS_NAME, send_message_field_class_name)
        send_message.send_keys(message)
        time.sleep(3)
        press_button = self.driver.find_element(By.CLASS_NAME, send_message_button_class_name)
        # press_button.click()
        time.sleep(5)


    def close(self):
        self.driver.quit()


