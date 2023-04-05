import time

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from browser.chrome_browser.options import CHROME_OPTIONS
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from browser import CookiesMixin
from selenium.webdriver import Chrome


class DriverChrome(Chrome, CookiesMixin):
    def __init__(self, options: Options = None, service: Service = None, time_sleep: int = 2):

        self.__link_by_default = 'https://www.google.com/'
        self.time_sleep = self.__verifity_time_sleep(time_sleep)
        super().__init__(options=options, service=service)

    def __str__(self):
        return f"Chrome browser: {self.__browser} Timing:  time_sleep = {self.time_sleep}"

    @staticmethod
    def __verifity_time_sleep(time_sleep: int):
        if isinstance(time_sleep, int):
            return time_sleep
        else:
            raise TypeError

    def set_time_sleep(self, time_sleep: int):
        self.time_sleep = self.__verifity_time_sleep(time_sleep)

    def sleep(self):
        if self.time_sleep > 0:
            time.sleep(self.time_sleep)


if __name__ == '__main__':
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    driver = DriverChrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.get('https://www.google.com/')
    driver.set_time_sleep(1)
    driver.sleep()
    driver.cookies_file_name = 'hello'
    print(driver.cookies_file_name)
    driver.set_time_sleep(1)
    driver.save_cookies_to_file()
    driver.set_time_sleep(1)
    print(driver.cookies_browser)
    driver.cookies_browser = False
    print(driver.cookies_browser)

