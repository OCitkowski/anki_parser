import os, time, random, json
from datetime import datetime
import logging

from dotenv import load_dotenv

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager
from sel_translate.main.chrome_browser.options import CHROME_OPTIONS
import redis


class ChromeBrowser():
    """Chrome __browser"""
    __type = "ChromeBrowser"

    def __init__(self):
        # super.__init__()

        self.__time_sleep = 60
        self.__link_by_default = 'https://www.google.com'
        self.__chrome_options = Options()
        self.chrome_options = CHROME_OPTIONS
        self.__browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                          options=self.__chrome_options)
        self.open()

    def __del__(self):
        # self.__close()
        pass

    def __str__(self):
        return f"Chrome browser: {self.__browser} Timing:  time_sleep = {self.__time_sleep}"

    @staticmethod
    def __verifity_time_sleep(time_sleep: int):
        if isinstance(time_sleep, int):
            return time_sleep
        else:
            raise TypeError

    @property
    def times_sleep(self):
        return {'time_sleep': self.__time_sleep}

    @times_sleep.setter
    def times_sleep(self, time_sleep: int):
        self.__time_sleep = self.__verifity_time_sleep(time_sleep)

    @property
    def chrome_options(self):
        # TODO simple
        chrome_options = []
        for i in self.__chrome_options:
            chrome_options.append(i)
        return chrome_options

    @chrome_options.setter
    def chrome_options(self, chrome_options):
        # TODO
        for i in chrome_options:
            self.__chrome_options.add_argument(i)

    @chrome_options.deleter
    def chrome_options(self):
        self.__options.arguments.clear()

    def open(self):
        self.__browser.get(self.__link_by_default)
        # self.__browser.refresh()
        self.sleep()

    def sleep(self):
        if self.__time_sleep > 0:
            time.sleep(self.__time_sleep)

    # def __close(self):
    #     self.__browser.close()


if __name__ == '__main__':
    Chr = ChromeBrowser()
