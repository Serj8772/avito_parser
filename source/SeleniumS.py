from selenium import webdriver
from selenium.webdriver.common.by import By
import fake_useragent
import time


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

    def get_attributes_list(self, elements_method_by, elements_value, element_method_by, element_value, attribute_name):
        attribute_list = []
        elements_list = self.driver.find_elements(elements_method_by, elements_value)
        for el in elements_list:
            attribute = el.find_element(element_method_by, element_value).get_attribute(attribute_name)
            if '?' in attribute:    # убираем лишние символы в ссылке
                attribute = attribute.split('?')[0]
            attribute_list.append(attribute)
        return attribute_list

    def close(self):
        self.driver.quit()