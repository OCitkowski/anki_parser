import random
import time
import redis
import logging
from multiprocessing import Pool

from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import PORT_REDIS, DB_PROXY_RADIS, CHROME_OPTIONS, NAME_COOKIES_FILE, MAX_CONCURRENT_TASKS, \
    TOTAL_TASKS, DB_WORDS_RADIS
from utils.redis_utils import get_sorted_rating_proxy_list, get_from_redis_word_all_data
from utils.cookies_utils import set_cookies_to_browser, save_cookies_to_file
from anki import get_urls_list
from handlers.handlers import find_element_s_by_xpath

# Створення об'єкта логування
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Створення обробника, який буде записувати логи в файл
handler = logging.FileHandler('verbformen.log')
handler.setLevel(logging.INFO)
# Створення форматувальника логів
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Додавання обробника до логера
logger.addHandler(handler)

redis_proxy_client = redis.Redis(host='localhost', port=PORT_REDIS, db=DB_PROXY_RADIS)

# urls = get_urls_list(TOTAL_TASKS)
data = []
for i, item in enumerate(get_from_redis_word_all_data(port=PORT_REDIS, db=DB_WORDS_RADIS)):
    if i > TOTAL_TASKS:
        break
    data.append(item)


def open_page(args):
    item = args
    url = item['URL']
    id = item['Id']
    word = item['Deutsch']

    proxies = get_sorted_rating_proxy_list(redis_proxy_client=redis_proxy_client,
                                           first_rating_proxy=MAX_CONCURRENT_TASKS)
    choice_proxy = random.choice(proxies)

    chrome_options = Options()
    for row in CHROME_OPTIONS:
        chrome_options.add_argument(row)

    if choice_proxy:
        proxy = Proxy({'proxyType': ProxyType.MANUAL,
                       'httpProxy': choice_proxy,
                       'noProxy': None,
                       'autodetect': False
                       })
        # створюємо об'єкт WebDriver з встановленим проксі
        chrome_options.add_argument(f'--proxy-server={choice_proxy}')

        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        proxy.add_to_capabilities(capabilities)

        logger.info(f'Start - {url} - {choice_proxy}')
    else:
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()

        logger.info(f'Run localhost- {url} // {choice_proxy} failed')

    driver = webdriver.Chrome(desired_capabilities=capabilities,
                              service=Service(ChromeDriverManager().install()),
                              options=chrome_options)

    try:
        driver.get(url)
        result = set_cookies_to_browser(driver, NAME_COOKIES_FILE)
        logger.info(f'set_cookies_to_browser- {url} // {result}')

        selector_I = "//*[@id='vVdBxBox']/p[(contains(@class,'rInf'))]"
        elements_I = find_element_s_by_xpath(driver, selector_I)
        driver.refresh()
        selector_II = "//*[@lang='uk']/span"
        elements_II = find_element_s_by_xpath(driver, selector_II)
        driver.refresh()
        selector_III = "//*[@id='vVdBxBox']/p[(contains(@class,'rInf'))]"
        elements_III = find_element_s_by_xpath(driver, selector_III)
        driver.refresh()
        selector_IV = "//*[@id='stammformen']"
        elements_IV = find_element_s_by_xpath(driver, selector_IV)
        print(id, word, elements_I, elements_II, elements_III, elements_IV)




        random_number = random.randint(3, 5)
        time.sleep(random_number)  # чекаємо random_number секунд, щоб сторінка повністю завантажилась

        save_cookies_to_file(driver, NAME_COOKIES_FILE)
        logger.info(f'End - {url} - {choice_proxy}')

        driver.quit()
    except Exception as ex:

        logger.error(f'Неочікувана зрада - - {url} - {choice_proxy} / {ex}')


if __name__ == '__main__':
    # run
    # python3 anki_parser/proxy_multiprocessing.py -free_proxy_txt 'anki_parser/free_proxy.txt' -max_concurrent_tasks 10

    try:
        pool = Pool(processes=MAX_CONCURRENT_TASKS)  # запускаємо не більше n процесів одночасно
        pool.map(open_page, data)
        pool.close()
        pool.join()
    except Exception as ex:

        logger.error(f'Неочікувана зрада - / {ex}')
    finally:
        pass
        # del_empty_row()
        # save_from_redis_items_to_words()
        # r.delete(NAME_REDIS_PROXY)
