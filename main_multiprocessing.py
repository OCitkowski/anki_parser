import random
import time, json
from multiprocessing import Pool
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from anki_parser.settings import CHROME_OPTIONS, MAX_CONCURRENT_TASKS, TOTAL_TASKS, REQUEST_TIMEOUT
from anki_parser.utilites import save_cookies_to_file, set_cookies_to_browser

urls = ['https://www.verbformen.ru/sklonenie/sushhestvitelnye/Heft.htm',
        'https://www.verbformen.ru/sklonenie/sushhestvitelnye/?w=hallen',
        'https://www.verbformen.ru/sklonenie/sushhestvitelnye/Heft.htm',
        'https://www.verbformen.ru/sklonenie/sushhestvitelnye/?w=hallen',
        'https://www.verbformen.ru/sklonenie/sushhestvitelnye/?w=hallen',
        'https://www.verbformen.ru/sklonenie/sushhestvitelnye/Heft.htm',
        'https://www.verbformen.ru/sklonenie/sushhestvitelnye/Heft.htm',
        'https://www.verbformen.ru/sklonenie/sushhestvitelnye/?w=hallen',
        'https://www.verbformen.ru/sklonenie/sushhestvitelnye/Heft.htm',
        'https://www.verbformen.ru/sklonenie/sushhestvitelnye/?w=hallen',

        ]


def open_page(url):
    service_log_path = "/home/fox/PycharmProjects/anki_parser/chromedriver.log"

    chrome_options = Options()
    for row in CHROME_OPTIONS:
        chrome_options.add_argument(row)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options,
                              service_log_path=service_log_path)

    set_cookies_to_browser(driver, 'verbformen')

    driver.get(url)

    random_number = random.randint(1, 10)
    time.sleep(random_number)  # чекаємо 5 секунд, щоб сторінка повністю завантажилась

    save_cookies_to_file(driver, 'verbformen')
    driver.quit()


if __name__ == '__main__':
    pool = Pool(processes=3)  # запускаємо не більше 3 процесів одночасно
    pool.map(open_page, urls)
    pool.close()
    pool.join()
