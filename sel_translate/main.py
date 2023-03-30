from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import threading
import time
import requests


class ProxyMixin:
    def __init__(self, proxy):
        self.proxy = proxy

    def set_proxy(self):
        if self.proxy:
            chrome_options = Options()
            chrome_options.add_argument(f'--proxy-server={self.proxy}')
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome()


class CookiesMixin:
    def __init__(self, cookies=None):
        self.cookies = cookies

    def set_cookies(self):
        if self.cookies:
            self.driver.get('https://www.google.com')
            for cookie in self.cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()


class MyThread(threading.Thread, ProxyMixin, CookiesMixin):
    def __init__(self, proxy, cookies):
        threading.Thread.__init__(self)
        ProxyMixin.__init__(self, proxy)
        CookiesMixin.__init__(self, cookies)

    def run(self):
        try:
            self.set_proxy()
            self.set_cookies()

            self.driver.get("https://www.google.com")
            search_box = self.driver.find_element_by_name("q")
            search_box.send_keys("ChromeDriver")
            search_box.submit()

            time.sleep(5)

            self.driver.quit()
        except:
            pass


cookies = [
    {'name': 'cookie1', 'value': '123'},
    {'name': 'cookie2', 'value': '456'},
    {'name': 'cookie3', 'value': '789'}
]

threads = []


def get_proxies_txt(filename):
    with open(filename + '.txt', 'r') as f:
        lines = f.readlines()
        # Відфільтровуємо перший рядок, який містить назву та дату
        lines = [line.strip() for line in lines if 'Free proxies' not in line and 'Updated' not in line]
        # Перетворюємо решту рядків з файлу на список проксі
        proxies = [line.strip() for line in lines if line.strip()]
    # print(proxies)
    return proxies


def check_proxy(proxy):
    try:
        response = requests.get('https://www.google.com', proxies={'https': proxy})
        if response.status_code == 200:
            print(f"Proxy {proxy} is working!")
        else:
            print(f"Proxy {proxy} is not working!")
    except:
        print(f"Proxy {proxy} is not working!")


if __name__ == '__main__':
    # logging.basicConfig(filename='_main.log', encoding='utf-8', datefmt='%Y-%m-%d_%H-%M-%S', level=logging.INFO)

    proxies = get_proxies_txt('free_proxy')

    # for proxy in proxies:
    #     thread = MyThread(proxy, cookies)
    #     threads.append(thread)
    #     thread.start()
    #
    # for thread in threads:
    #     thread.join()

    threads = []
    max_threads = 10
    threads_created = 0

    for proxy in proxies:
        thread = MyThread(proxy, cookies)
        threads.append(thread)
        thread.start()
        threads_created += 1
        if threads_created >= max_threads:
            break

    for thread in threads:
        thread.join()
