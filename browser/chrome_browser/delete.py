# import multiprocessing
# import time
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from sel_translate.main.chrome_browser.options import CHROME_OPTIONS
# from selenium.webdriver.chrome.service import Service
#
#
# class ChromeBrowser():
#     """Chrome __browser"""
#     __type = "ChromeBrowser"
#
#     def __init__(self, open_browser=False, times_sleep: int = 5):
#         # super.__init__()
#
#         self.__time_sleep = times_sleep
#         self.__link_by_default = 'https://www.google.com'
#         self.__chrome_options = Options()
#         self.chrome_options = CHROME_OPTIONS
#         self.__browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
#                                           options=self.__chrome_options)
#         if open_browser:
#             self.open()
#
#     def __str__(self):
#         return f"Chrome browser: {self.__browser} Timing:  time_sleep = {self.__time_sleep}"
#
#     @staticmethod
#     def __verifity_time_sleep(time_sleep: int):
#         if isinstance(time_sleep, int):
#             return time_sleep
#         else:
#             raise TypeError
#
#     @property
#     def times_sleep(self):
#         return {'time_sleep': self.__time_sleep}
#
#     @times_sleep.setter
#     def times_sleep(self, time_sleep: int):
#         self.__time_sleep = self.__verifity_time_sleep(time_sleep)
#
#     @property
#     def chrome_options(self):
#         # TODO simple
#         chrome_options = []
#         for i in self.__chrome_options:
#             chrome_options.append(i)
#         return chrome_options
#
#     @chrome_options.setter
#     def chrome_options(self, chrome_options):
#         # TODO
#         for i in chrome_options:
#             self.__chrome_options.add_argument(i)
#
#     @chrome_options.deleter
#     def chrome_options(self):
#         self.__options.arguments.clear()
#
#     def open(self):
#         self.__browser.get(self.__link_by_default)
#         self.sleep()
#
#     def sleep(self):
#         if self.__time_sleep > 0:
#             time.sleep(self.__time_sleep)
#
#     def close(self):
#         self.__browser.close()
#
#
# def start_chrome_process(process_id):
#     chrome = ChromeBrowser(open_browser=True, times_sleep=5)
#     print(f"Chrome process {process_id} started.")
#     chrome.sleep()  # wait for some time
#     chrome.close()  # quit the driver
#
#
# if __name__ == '__main__':
#     num_processes = 10
#     num_concurrent_processes = 10
#
#     process_list = []
#     for i in range(num_processes):
#         process = multiprocessing.Process(target=start_chrome_process, args=(i,))
#         process_list.append(process)
#
#     for i in range(0, num_processes, num_concurrent_processes):
#         concurrent_processes = process_list[i:i + num_concurrent_processes]
#         for process in concurrent_processes:
#             process.start()
#         for process in concurrent_processes:
#             process.join()
#
#     print("All Chrome processes finished.")

class Chr():

    def __init__(self):
        print(self.__class__.__name__)


import multiprocessing, time
from selenium import webdriver


def scrape(url):
    driver = webdriver.Chrome()
    driver.get(url)
    page_source = driver.page_source
    time.sleep(5)
    driver.close()
    # do something with the page source


if __name__ == '__main__':

    urls = [
        'https://en.wikipedia.org/wiki/0',
        'https://en.wikipedia.org/wiki/1',
        'https://en.wikipedia.org/wiki/2',
        'https://en.wikipedia.org/wiki/3',
    ]

    processes = []
    for url in urls:
        p = multiprocessing.Process(target=scrape, args=(url,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
