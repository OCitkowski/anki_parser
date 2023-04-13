import random
import time, json
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.proxy import *

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from anki_parser.settings import CHROME_OPTIONS, CSS_SELECTOR, NAME_REDIS_PROXY, NAME_COOKIES_FILE, \
    MAX_CONCURRENT_TASKS, TOTAL_TASKS, NAME_JSON_WORDS_FILE
from anki_parser.utilites import save_cookies_to_file, set_cookies_to_browser, find_elements_by_css_to_list, \
    get_urls_from_file, set_to_redis_words_trans_list, save_from_redis_items_to_words
import redis

from urllib.parse import urlparse, parse_qs

r = redis.Redis(host='localhost', port=6379, db=0)
r.ping()

urls_test = ['https://dict.com/ukrainisch-deutsch/noch',
             'https://dict.com/ukrainisch-deutsch/sein',
             'https://dict.com/ukrainisch-deutsch/morgen',
             'https://dict.com/ukrainisch-deutsch/haben',
             'https://dict.com/ukrainisch-deutsch/muss',
             'https://dict.com/ukrainisch-deutsch/soll',
             ]
urls = get_urls_from_file(json_file_words=NAME_JSON_WORDS_FILE, count_items=TOTAL_TASKS)


def open_page(url):
    service_log_path = "/home/fox/PycharmProjects/anki_parser/chromedriver.log"

    chrome_options = Options()
    for row in CHROME_OPTIONS:
        chrome_options.add_argument(row)

    items = r.lrange(NAME_REDIS_PROXY, 0, -1)
    decoded_proxy_list = [item.decode('utf-8') for item in items]


    if decoded_proxy_list:
        choice_proxy_list = random.choice(decoded_proxy_list)

        proxy = Proxy({'proxyType': ProxyType.MANUAL,
                       'httpProxy': choice_proxy_list,
                       'noProxy': None,
                       'autodetect': False
                       })
        # створюємо об'єкт WebDriver з встановленим проксі
        chrome_options.add_argument(f'--proxy-server={choice_proxy_list}')

        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        proxy.add_to_capabilities(capabilities)
        print(f'Run {choice_proxy_list} -----------')
    else:
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        print(f'Run localhost -----------')

    driver = webdriver.Chrome(desired_capabilities=capabilities,
                              service=Service(ChromeDriverManager().install()),
                              options=chrome_options,
                              service_log_path=service_log_path)

    driver.get(url)
    set_cookies_to_browser(driver, NAME_COOKIES_FILE)

    found_elements = find_elements_by_css_to_list(driver=driver, element_css_names=CSS_SELECTOR)
    print(found_elements)

    parsed_url = urlparse(url)
    url_params = parse_qs(parsed_url.query)

    print(url, url_params, url_params['id'])
    # save_item_in_json_file(found_elements, NAME_JSON_WORDS_FILE, url_params)
    set_to_redis_words_trans_list(found_elements, url_params)

    random_number = random.randint(3, 5)
    time.sleep(random_number)  # чекаємо random_number секунд, щоб сторінка повністю завантажилась

    # save_cookies_to_file(driver, NAME_COOKIES_FILE)
    driver.quit()

    # get_redis_words_trans_list()


if __name__ == '__main__':
    # run
    # python3 anki_parser/proxy_multiprocessing.py -free_proxy_txt 'anki_parser/free_proxy.txt' -max_concurrent_tasks 10

    pool = Pool(processes=MAX_CONCURRENT_TASKS)  # запускаємо не більше n процесів одночасно
    pool.map(open_page, urls)
    pool.close()
    pool.join()

    save_from_redis_items_to_words()

    # r.delete(NAME_REDIS_PROXY)
