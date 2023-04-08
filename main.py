import time, json
from multiprocessing import Pool
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from anki_parser.options import CHROME_OPTIONS, MAX_CONCURRENT_TASKS, TOTAL_TASKS, REQUEST_TIMEOUT


def open_page(url):

    chrome_options = webdriver.ChromeOptions()
    for row in CHROME_OPTIONS:
        chrome_options.add_argument(row)

    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

    driver.get(url)
    time.sleep(10)  # чекаємо 5 секунд, щоб сторінка повністю завантажилась

    driver.quit()


if __name__ == '__main__':
    urls = ['https://dict.com/ukrainisch-deutsch/hallo',
            'https://dict.com/ukrainisch-deutsch/Strafe',
            'https://dict.com/ukrainisch-deutsch/anderer',
            'https://dict.com/ukrainisch-deutsch/deutsch',
            # тут ще 100 urls
            ]

    pool = Pool(processes=2)  # запускаємо не більше 3 процесів одночасно
    pool.map(open_page, urls)
    pool.close()
    pool.join()
    # open_page('https://dict.com/ukrainisch-deutsch/hallo')