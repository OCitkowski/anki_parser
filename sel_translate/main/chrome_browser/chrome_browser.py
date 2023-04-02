import time, multiprocessing
from multiprocessing.pool import ThreadPool as Pool

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from sel_translate.main.chrome_browser.options import CHROME_OPTIONS


class ChromeBrowser():
    """Chrome __browser"""
    __type = "ChromeBrowser"

    def __init__(self, open_browser=False, times_sleep: int = 60):
        # super.__init__()

        self.__time_sleep = times_sleep
        self.__link_by_default = 'https://www.google.com'
        self.__chrome_options = Options()
        self.chrome_options = CHROME_OPTIONS
        self.__browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                          options=self.__chrome_options)
        if open_browser:
            self.open()

    def __str__(self):
        return f"Chrome browser: {self.__browser} Timing:  time_sleep = {self.__time_sleep}"

    # def __del__(self):
    #     self.close()

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
        self.sleep()

    def sleep(self):
        if self.__time_sleep > 0:
            time.sleep(self.__time_sleep)

    def close(self):
        self.__browser.close()
        self.__browser.quit()


def main(times_sleep, open_browser):
    chrome = ChromeBrowser(open_browser=open_browser, times_sleep=times_sleep)


def wrapper(args):
    main(times_sleep=args['times_sleep'], open_browser=args['open_browser'])


if __name__ == '__main__':

    # start = []
    # for i in range(5):
    #     start.append({'times_sleep': 10, 'open_browser': True})
    #
    # with Pool(processes=5) as pool:
    #     pool.map(wrapper, start)

    processes = []
    for i in range(5):
        start_args = ({'times_sleep': 10, 'open_browser': True})
        p = multiprocessing.Process(target=wrapper, args=(start_args,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
