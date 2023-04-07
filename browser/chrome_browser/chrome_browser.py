import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from browser import CookiesMixin, OptionsMixin
from selenium.webdriver import Chrome


class DriverChrome(Chrome, CookiesMixin, OptionsMixin):
    def __init__(self, time_sleep: int = 2, proxy: str = None):

        chrome_options = self.set_chrome_options_mixin()
        if proxy != None:
            chrome_options.add_argument(f'--proxy-server={proxy}')

        self.__link_by_default = 'https://www.google.com/'
        self.time_sleep = self.__verifity_time_sleep(time_sleep)
        super().__init__(options=chrome_options,
                         service=Service(ChromeDriverManager().install()))

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

    def sleep(self, time_sleep: int = None):
        if time_sleep == None:
            if self.time_sleep > 0:
                time.sleep(self.time_sleep)
        else:
            time.sleep(time_sleep)


if __name__ == '__main__':
    driver = DriverChrome(10)
    driver.get('https://www.google.com/')
    driver.sleep()
    driver.cookies_file_name = 'hello'

    driver.save_cookies_to_file()
    driver.cookies_browser = False  # TODO
