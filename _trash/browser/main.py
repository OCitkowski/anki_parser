from multiprocessing import Process
import random

from _trash.browser.chrome_browser.chrome_browser import DriverChrome
import requests

from _trash.browser.chrome_browser.options import REQUEST_TIMEOUT

links_test = ['https://dict.com/ukrainisch-deutsch/hallo',
              'https://dict.com/ukrainisch-deutsch/Strafe',
              'https://dict.com/ukrainisch-deutsch/anderer',
              'https://dict.com/ukrainisch-deutsch/deutsch']

urls = [
    'https://en.wikipedia.org/wiki/0',
    'https://en.wikipedia.org/wiki/1',
    'https://en.wikipedia.org/wiki/2',
    'https://en.wikipedia.org/wiki/3',
]


class TranslateBot(DriverChrome):
    _count = 0
    def __init__(self, proxy: str = None):
        TranslateBot._count += 1
        self.name = f"instance_{TranslateBot._count}"
        super().__init__(proxy=proxy)
        print(self.__repr__())  # = hex(id(self))
        print(id(self))



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


def main(times_sleep, proxy, link, item):
    driver = TranslateBot(proxy=proxy)
    # name = f'driver_{item}'
    # exec(f'{name} = TranslateBot(proxy={proxy})')

    # cookies_file_name = 'new-None'
    # name.cookies_browser = cookies_file_name

    # driver.cookies_browser = cookies_file_name
    # driver.get(link)
    driver.sleep(times_sleep)
    #
    # for l in links_test:
    #     driver.get(l)
    #     driver.sleep(times_sleep)
    #
    #
    # driver.save_cookies_to_file(cookies_file_name)
    # driver.cookies_browser = False  # TODO


def wrapper(args):
    main(times_sleep=args['times_sleep'], proxy=args['proxy'], link=args['link'], item=args['item'])


if __name__ == '__main__':
    processes = []

    for i, link in enumerate(urls):
        proxy = random.choice(get_proxies_from_txt('free_proxy_test.txt'))

        start_args = ({'times_sleep': 5, 'proxy': proxy, 'link': link, 'item': i})
        p = Process(target=wrapper, args=(start_args,))
        p.start()
        processes.append(p)
        print(proxy)

    for p in processes:
        p.join()
