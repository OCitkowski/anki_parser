# import time, json
# from multiprocessing import Pool
# from selenium import webdriver
#
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
#
# from anki_parser.options import CHROME_OPTIONS, MAX_CONCURRENT_TASKS, TOTAL_TASKS, REQUEST_TIMEOUT
#
#
# def open_page(url):
#
#     chrome_options = webdriver.ChromeOptions()
#     for row in CHROME_OPTIONS:
#         chrome_options.add_argument(row)
#
#     driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
#
#     driver.get(url)
#     time.sleep(10)  # чекаємо 5 секунд, щоб сторінка повністю завантажилась
#
#     driver.quit()
#
#
# if __name__ == '__main__':
#
#
#     pool = Pool(processes=2)  # запускаємо не більше 3 процесів одночасно
#     pool.map(open_page, urls)
#     pool.close()
#     pool.join()
#     # open_page('https://dict.com/ukrainisch-deutsch/hallo')
import asyncio
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import redis

from anki_parser.options import CHROME_OPTIONS, MAX_CONCURRENT_TASKS, TOTAL_TASKS, REQUEST_TIMEOUT

urls = ['https://dict.com/ukrainisch-deutsch/hallo',
        'https://dict.com/ukrainisch-deutsch/Strafe',
        'https://dict.com/ukrainisch-deutsch/anderer',
        'https://dict.com/ukrainisch-deutsch/deutsch',
        # тут ще 100 urls
        ]

chrome_options = Options()
for row in CHROME_OPTIONS:
    chrome_options.add_argument(row)
service = Service(ChromeDriverManager().install())

redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)  # підключення до Redis
r = redis.Redis(connection_pool=redis_pool)


async def parse_page(url):
    driver = webdriver.Chrome(options=chrome_options, service=service)  # ініціалізація драйвера
    driver.get(url)  # отримання сторінки
    # код для отримання необхідних даних

    random_number = random.randint(5, 10)
    await asyncio.sleep(random_number)

    # збереження даних у Redis

    r.set('my_key', random_number)
    driver.quit()  # закриття драйвера


async def main():
    tasks = [parse_page(url) for url in urls]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f'Time taken: {end - start} seconds')
