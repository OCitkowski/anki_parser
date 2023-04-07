import multiprocessing
from browser.chrome_browser.chrome_browser import DriverChrome
import requests

from browser.chrome_browser.options import REQUEST_TIMEOUT


class Browser(DriverChrome):
    def __init__(self, proxy: str = None):
        super().__init__(proxy=proxy)


def get_proxis_from_txt(filename):
    proxies = []
    try:

        with open(filename, 'r') as f:
            lines = f.readlines()

            for line in lines:
                proxies.append(line)
    except Exception as e:
        pass
    finally:
        f.close()
    return proxies

def check_proxy(proxy):
    try:
        response = requests.get('https://www.google.com', proxies={'https': proxy.rstrip('\n')},
                                timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def main(times_sleep, proxy):
    driver = Browser(proxy=proxy)
    driver.get('https://www.google.com/')
    driver.sleep(5)
    driver.cookies_file_name = 'hello'
    driver.save_cookies_to_file()
    driver.cookies_browser = False  # TODO


def wrapper(args):
    main(times_sleep=args['times_sleep'], proxy=args['proxy'])


if __name__ == '__main__':

    # start = []
    # for i in range(5):
    #     start.append({'times_sleep': 10, 'open_browser': True})
    #
    # with multiprocessing.Pool(processes=5) as pool:
    #     pool.map(wrapper, start)

    processes = []
    # for i in range(10):
    for proxy in get_proxis_from_txt('free_proxy_test.txt'):
        if check_proxy(proxy):
            start_args = ({'times_sleep': 20, 'proxy': proxy})
            p = multiprocessing.Process(target=wrapper, args=(start_args,))
            p.start()
            processes.append(p)
            print(proxy)

    for p in processes:
        p.join()
