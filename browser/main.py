import multiprocessing
from browser.chrome_browser.chrome_browser import DriverChrome


class Browser(DriverChrome):
    def __init__(self):
        super().__init__(time_sleep=5)


def main(times_sleep, open_browser):
    driver = Browser()
    driver.get('https://www.google.com/')
    driver.sleep()
    driver.cookies_file_name = 'hello'
    driver.save_cookies_to_file()
    driver.cookies_browser = False  # TODO


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
    for i in range(2):
        start_args = ({'times_sleep': 20, 'open_browser': False})
        p = multiprocessing.Process(target=wrapper, args=(start_args,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
