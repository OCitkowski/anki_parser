import asyncio
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests

MAX_THREADS = 10


class ProxyMixin:
    def __init__(self, proxy=None):
        self.proxy = proxy

    async def set_proxy(self):
        if self.proxy:
            chrome_options = Options()
            chrome_options.add_argument(f'--proxy-server={self.proxy}')
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome()

    async def check_proxy(self):
        try:
            await asyncio.wait_for(self.driver.get('https://httpbin.org/get'), timeout=5)
            return True
        except:
            return False


class CookiesMixin:
    def __init__(self, cookies=None):
        self.cookies = cookies

    async def set_cookies(self):
        if self.cookies:
            self.driver.get('https://www.google.com')
            for cookie in self.cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()


async def test_proxy(proxy, cookies):
    proxy_mixin = ProxyMixin(proxy)
    await proxy_mixin.set_proxy()

    if await proxy_mixin.check_proxy():
        cookies_mixin = CookiesMixin(cookies)
        await cookies_mixin.set_cookies()

        proxy_mixin.driver.get('https://www.google.com')
        search_box = proxy_mixin.driver.find_element_by_name('q')
        search_box.send_keys('ChromeDriver')
        search_box.submit()

        await asyncio.sleep(randint(1, 5))
        proxy_mixin.driver.quit()


async def main():
    proxies = get_proxies_txt('free_proxy')

    cookies = [
        {'name': 'cookie1', 'value': '123'},
        {'name': 'cookie2', 'value': '456'},
        {'name': 'cookie3', 'value': '789'}
    ]

    tasks = []
    sem = asyncio.Semaphore(MAX_THREADS)

    # async with sem:
    for proxy in proxies:
        async with sem:
            task = asyncio.create_task(test_proxy(proxy, cookies))
            tasks.append(task)

    await asyncio.gather(*tasks)





if __name__ == '__main__':
    # logging.basicConfig(filename='_main.log', encoding='utf-8', datefmt='%Y-%m-%d_%H-%M-%S', level=logging.INFO)
    #
    # proxies = get_proxies_txt('free_proxy')

    asyncio.run(main())
