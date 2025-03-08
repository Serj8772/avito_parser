import requests
from bs4 import BeautifulSoup
import fake_useragent
import time


class BS:
    def __init__(self, url, use_fake_useragent=True):
        self.url = url
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        headers = {}
        if use_fake_useragent:
            ua = fake_useragent.UserAgent(os=["Windows", "Chrome OS", "Mac OS X"]).random
            headers['User-Agent'] = ua
            print(headers)
        self.html = requests.get(self.url, headers=headers)

    def get_links(self, div_class='iva-item-title-CdRXl', a_class='styles-module-root-m3BML'):
        links = []
        items = self.soup.find_all('div', class_=div_class)
        for item in items:
            link = item.find('a', class_=a_class)['href']
            if '?' in link:    # убираем лишние символы в ссылке
                link = f'https://www.avito.ru{link.split("?")[0]}'
            links.append(link)
        return links


if __name__ == '__main__':
    link = 'https://www.avito.ru/lobnya/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?context=H4sIAAAAAAAA_wEjANz_YToxOntzOjg6ImZyb21QYWdlIjtzOjc6ImNhdGFsb2ciO312FITcIwAAAA&f=ASgBAgICA0SSA8gQ8AeQUrCzFP6hjwM&s=104'
    avito_bs = BS(link)
    print(avito_bs.get_links())

