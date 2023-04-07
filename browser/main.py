import multiprocessing
import random

from browser.chrome_browser.chrome_browser import DriverChrome
import requests

from browser.chrome_browser.options import REQUEST_TIMEOUT


class TranslateBot(DriverChrome):
    def __init__(self, proxy: str = None):
        super().__init__(proxy=proxy)


def get_proxies_from_txt(file_name: str) -> list:
    proxies = []
    try:
        with open(file_name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                proxies.append(line)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    return proxies


def delete_bad_proxies_from_txt(file_name: str) -> None:
    try:
        with open(file_name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if check_proxy(line):
                    pass
                else:
                    lines.remove(line)
            with open(file_name, 'w') as f:
                f.write("".join(lines))
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")


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


def main(times_sleep, proxy, link):
    driver = TranslateBot(proxy=proxy)
    driver.get('https://www.google.com/')
    driver.sleep(5)
    driver.cookies_file_name = 'hello'
    driver.save_cookies_to_file()
    driver.cookies_browser = False  # TODO


def wrapper(args):
    main(times_sleep=args['times_sleep'], proxy=args['proxy'])


if __name__ == '__main__':
    # processes = []
    # # for i in range(10):
    # for proxy in random.choice(get_proxies_from_txt('free_proxy_test.txt')):
    #     start_args = ({'times_sleep': 20, 'proxy': proxy})
    #     p = multiprocessing.Process(target=wrapper, args=(start_args,))
    #     p.start()
    #     processes.append(p)
    #     print(proxy)
    #
    # for p in processes:
    #     p.join()

    filename = 'free_proxy_test.txt'
    delete_bad_proxies_from_txt(filename)
    pr = get_proxies_from_txt(filename)
    print(pr)
    print(random.choice(pr))
