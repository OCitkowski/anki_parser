import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from browser.chrome_browser.options import  CHROME_OPTIONS


class ChromeBrowser():
    """Chrome __browser"""
    __type = "ChromeBrowser"

    def __init__(self, open_browser=False, times_sleep: int = 60):

        super().__init__()
        self.__link_by_default = 'https://www.google.com'
        self.__options = Options()
        self.__chrome_options = CHROME_OPTIONS
        self.__browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                          options=self.__options)

        self.time_sleep = times_sleep
        if open_browser:
            self.open()

    def __str__(self):
        return f"Chrome browser: {self.__browser} Timing:  time_sleep = {self.time_sleep}"

    @staticmethod
    def __verifity_time_sleep(time_sleep: int):
        if isinstance(time_sleep, int):
            return time_sleep
        else:
            raise TypeError

    @property
    def times_sleep(self):
        return {'time_sleep': self.time_sleep}

    @times_sleep.setter
    def times_sleep(self, time_sleep: int):
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


class Bro(ChromeBrowser):
    def __init__(self, open_browser=False, times_sleep: int = 60):
        super().__init__()
        self.time_sleep = times_sleep
        if open_browser:
            self.open()


if __name__ == '__main__':
    bro = Bro(open_browser=True, times_sleep=10)
