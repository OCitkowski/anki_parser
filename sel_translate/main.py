import os, time, random, json

from dotenv import load_dotenv

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager
from browser_options import CHROME_OPTIONS

load_dotenv()
password = os.getenv("PASSWORD")
user_name = os.getenv("USER_NAME")


class ChromeBrowser():
    """Chrome __browser"""
    __type = "ChromeBrowser"

    def __init__(self):
        self.__browser = None
        self.__chrome_options = Options()
        self._cookies_file_name = 'chrome'
        self._cookies = 'None'
        self._json_file_name = 'chrome'
        self.__max_time_sleep = 0
        self.__min_time_sleep = 0
        self.__hand_time_sleep = 0

    def __del__(self):
        if self.__browser:
            self.__close()

    def __str__(self):
        return f"Chrome __browser: {self.__browser} Timing: max = {self.__max_time_sleep}  min = {self.__min_time_sleep}  hand = {self.__hand_time_sleep}"

    @staticmethod
    def __verifity_time_sleep(time_sleep: int):
        if isinstance(time_sleep, int):
            return time_sleep
        else:
            raise TypeError

    @staticmethod
    def __verifity_file_name(file_name: str):
        if isinstance(file_name, str):
            return file_name
        else:
            raise TypeError

    @staticmethod
    def print_type():
        print(ChromeBrowser.__type)

    def get_times_sleep(self) -> dict:
        return {'hand_time': self.__hand_time_sleep, 'min': self.__min_time_sleep, 'max': self.__max_time_sleep}

    def set_times_sleep(self, hand_time_sleep: int = 0, min_time_sleep: int = 0, max_time_sleep: int = 0):
        if self.__verifity_time_sleep(hand_time_sleep) > 0:
            self.__hand_time_sleep = hand_time_sleep
            self.__min_time_sleep = 0
            self.__max_time_sleep = 0

        if self.__verifity_time_sleep(hand_time_sleep) == 0 \
                and self.__verifity_time_sleep(min_time_sleep) <= self.__verifity_time_sleep(max_time_sleep):
            self.__min_time_sleep = min_time_sleep
            self.__max_time_sleep = max_time_sleep

    @property
    def cookies_file_name(self):
        return self._cookies_file_name

    @cookies_file_name.setter
    def cookies_file_name(self, file_name: str):
        self._cookies_file_name = self.__verifity_file_name(file_name)

    @cookies_file_name.deleter
    def cookies_file_name(self):
        self._cookies_file_name = ''

    @property
    def json_file_name(self):
        return self._json_file_name

    @json_file_name.setter
    def json_file_name(self, file_name: str):
        self._json_file_name = self.__verifity_file_name(file_name)

    @json_file_name.deleter
    def json_file_name(self):
        self._json_file_name = ''

    @property
    def chrome_options(self):
        chrome_options = []
        for i in self.__chrome_options.arguments:
            chrome_options.append(i)
        return chrome_options

    @chrome_options.setter
    def chrome_options(self, options):

        self.__chrome_options.add_argument("--disable-extensions")
        for option in options:
            self.__chrome_options.add_argument(option)

        self.__browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                          options=self.__chrome_options)

    @chrome_options.deleter
    def chrome_options(self):
        self.__chrome_options.arguments.clear()

    def del_cookies_browser(self) -> bool:
        result = False
        try:
            self.__browser.delete_all_cookies()
            result = True
        except:
            self.__browser.refresh()

        return result

    def set_cookies_to_browser(self) -> bool:
        result = False
        try:
            self.__browser.delete_all_cookies()
            cookies = json.load(open(f"{self._cookies_file_name}.cookies", "r"))
            for cookie in cookies:
                try:
                    self.__browser.add_cookie(cookie)
                    result = True
                    print(cookie)
                except Exception as ex:
                    print(ex)
        except:
            self.__browser.refresh()
            result = False
        finally:
            print(f'set cookies is {result}')
            return result

    def save_cookies_to_file(self) -> bool:
        result = False
        try:
            print(self._cookies_file_name)
            with open(self._cookies_file_name + '.cookies', 'w') as write_file:
                json.dump(self.__browser.get_cookies(), write_file, ensure_ascii=False)
                result = True
            print(f'{self._cookies_file_name}.cookies save to root')
        except Exception as ex:
            print(f'{self._cookies_file_name}.cookies don`t save to root : {ex}')
        return result

    def save_data_in_json_file(self, data):
        result = False
        try:
            with open(self._json_file_name + '.json', 'w') as write_file:
                json.dump(data, write_file, ensure_ascii=False)
                result = True
            print(f'{self._json_file_name}.json save to root')
        except:
            print(f'{self._json_file_name}.json don`t save to root')
        return result

    def get_data_from_json_file(self):
        result = False
        try:
            with open(self._json_file_name + '.json', 'r') as read_file:
                result = json.load(read_file)
            print(f'{self._json_file_name}.json get data from json file')
        except:
            print(f'{self._json_file_name}.json don`t get data from json file')
        return result

    def open(self):
        return self.__browser

    def sleep(self):
        if self.__hand_time_sleep > 0:
            time.sleep(self.__hand_time_sleep)
        else:
            time.sleep(random.randrange(self.__min_time_sleep, self.__max_time_sleep))

    def xpath_exists(self, xpath):
        try:
            self.__browser.find_element(By.XPATH, xpath)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def __close(self):
        if self._cookies_file_name:
            self.save_cookies_to_file()
        self.__browser.close()


class TranslateBot(ChromeBrowser):
    """Translatem Bot"""
    __type = "Translate"

    def __init__(self, username, password, ):
        super().__init__()
        self.username = username
        self.password = password
        self.__link_by_default = 'https://dict.com/%D0%BD%D1%96%D0%BC%D0%B5%D1%86%D1%8C%D0%BA%D0%BE-%D1%83%D0%BA%D1%80%D0%B0%D1%96%D0%BD%D1%81%D1%8C%D0%BA%D0%B8%D0%B8/hallo'

    def open_by_word(self):
        self.__browser = self.open()
        if not self.__link_by_default == None:
            self.__browser.get(self.__link_by_default)
            self.set_cookies_to_browser()
            # self.__browser.refresh()
            self.sleep()


if __name__ == '__main__':
    # try:
    full_file_name = '_x.py'
    translate = TranslateBot(username=user_name, password=password)
    translate.cookies_file_name = user_name + '_translate'
    translate.set_times_sleep(hand_time_sleep=0, min_time_sleep=3, max_time_sleep=7)
    translate.chrome_options = CHROME_OPTIONS
    translate.open_by_word()
    translate.set_times_sleep(hand_time_sleep=10)
    # translate.del_cookies_browser()
    translate.save_cookies_to_file()
