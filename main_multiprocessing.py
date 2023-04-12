import random
import time, json
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.proxy import *

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from anki_parser.settings import CHROME_OPTIONS, HTTP_PROXY_LIST, CSS_SELECTOR, MAX_CONCURRENT_TASKS, TOTAL_TASKS, \
    REQUEST_TIMEOUT
from anki_parser.utilites import save_cookies_to_file, set_cookies_to_browser, find_elements_by_css_to_list, \
    set_to_redis_proxy_list
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
r.ping()
name_redis_proxy_list = 'check_proxy_list'

urls = ['https://dict.com/ukrainisch-deutsch/noch',
        'https://dict.com/ukrainisch-deutsch/sein',
        'https://dict.com/ukrainisch-deutsch/morgen',
        'https://dict.com/ukrainisch-deutsch/haben',
        'https://dict.com/ukrainisch-deutsch/muss',
        'https://dict.com/ukrainisch-deutsch/soll',
        ]

cookies_file_name = 'cookies'


def open_page(url, choice_proxy_list=None):
    service_log_path = "/home/fox/PycharmProjects/anki_parser/chromedriver.log"

    chrome_options = Options()
    for row in CHROME_OPTIONS:
        chrome_options.add_argument(row)

    items = r.lrange(name_redis_proxy_list, 0, -1)
    decoded_items = [item.decode('utf-8') for item in items]

    choice_proxy_list = random.choice(decoded_items)
    print(choice_proxy_list)

    proxy = Proxy({'proxyType': ProxyType.MANUAL,
                   'httpProxy': choice_proxy_list,
                   'noProxy': None,
                   'autodetect': False
                   })

    # створюємо об'єкт WebDriver з встановленим проксі
    chrome_options.add_argument(f'--proxy-server={choice_proxy_list}')

    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    proxy.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(desired_capabilities=capabilities,
                              service=Service(ChromeDriverManager().install()),
                              options=chrome_options,
                              service_log_path=service_log_path)

    driver.get(url)
    set_cookies_to_browser(driver, cookies_file_name)

    found_elements = find_elements_by_css_to_list(driver=driver, element_css_names=CSS_SELECTOR)
    print(found_elements)

    random_number = random.randint(3, 5)
    time.sleep(random_number)  # чекаємо random_number секунд, щоб сторінка повністю завантажилась

    save_cookies_to_file(driver, cookies_file_name)
    driver.quit()


if __name__ == '__main__':
    r.delete(name_redis_proxy_list)
    set_to_redis_proxy_list(proxy_list=HTTP_PROXY_LIST, name_redis_proxy_list=name_redis_proxy_list)

    pool = Pool(processes=5)  # запускаємо не більше n процесів одночасно
    pool.map(open_page, urls)
    pool.close()
    pool.join()
