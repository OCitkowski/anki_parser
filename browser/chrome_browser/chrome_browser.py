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


class ChromeBrowser():
    """Chrome __browser"""
    __type = "ChromeBrowser"

    def __init__(self):

        super().__init__()
        self.__link_by_default = 'https://www.google.com'
        self.__options = Options()
        self.__chrome_options = CHROME_OPTIONS
        self.__browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                          options=self.__options, )
        self.time_sleep

    def __str__(self):
        return f"Chrome browser: {self.__browser} Timing:  time_sleep = {self.time_sleep}"

    @staticmethod
    def __verifity_time_sleep(time_sleep: int):
        if isinstance(time_sleep, int):
            return time_sleep
        else:
            raise TypeError

    @property
    def time_sleep(self):
        return {'time_sleep': self.time_sleep}

    @time_sleep.setter
    def time_sleep(self, time_sleep: int):
        self.time_sleep = self.__verifity_time_sleep(time_sleep)

    @property
    def __chrome_options(self):
        # TODO simple
        chrome_options = []
        for i in self.__options:
            chrome_options.append(i)
        return chrome_options

    @__chrome_options.setter
    def __chrome_options(self, chrome_options):
        # TODO
        for i in chrome_options:
            self.__options.add_argument(i)

    @__chrome_options.deleter
    def __chrome_options(self):
        self.__options.arguments.clear()

    def open(self):
        self.__browser.get(self.__link_by_default)
        self.sleep()

    def sleep(self):
        if self.time_sleep > 0:
            print(self.__browser)
            time.sleep(self.time_sleep)

    def close(self):
        self.__browser.close()
        self.__browser.quit()


class DriverChrome(Chrome):
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

    def open(self):
        self.get(self.__link_by_default)
        self.sleep()

    def sleep(self):
        if self.time_sleep > 0:
            time.sleep(self.time_sleep)



if __name__ == '__main__':
    options = Options()
    # options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service_args = {key: val for key, val in options.to_capabilities()['goog:chromeOptions'].items()}

    driver = DriverChrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.open()
