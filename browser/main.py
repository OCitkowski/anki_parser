import multiprocessing
from chrome_browser.chrome_browser import ChromeBrowser
from mixin.mixin import CookiesMixin


class Browser(ChromeBrowser, CookiesMixin):
    """Chrome __browser"""
    __type = "ChromeBrowser"

    def __init__(self, open_browser=False, times_sleep: int = 60, *args):
        super().__init__(*args)
        self.time_sleep = times_sleep
        if open_browser:
            self.open()


def main(times_sleep, open_browser):
    chrome = Browser(open_browser=open_browser, times_sleep=times_sleep)
    chrome.sleep()



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
