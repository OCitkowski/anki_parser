import asyncio
import json
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import redis

from verbformen_parser.settings import CHROME_OPTIONS, MAX_CONCURRENT_TASKS, TOTAL_TASKS, REQUEST_TIMEOUT
from verbformen_parser.utilites import save_cookies_to_file, set_cookies_to_browser

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

chrome_options = Options()
for row in CHROME_OPTIONS:
    chrome_options.add_argument(row)
service = Service(ChromeDriverManager().install())
service_log_path = "/home/fox/PycharmProjects/anki_parser/chromedriver.log"

redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)  # підключення до Redis
r = redis.Redis(connection_pool=redis_pool)


async def parse_page(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options,
                              service_log_path=service_log_path)

    set_cookies_to_browser(driver, 'cooc_as')
    driver.get(url)  # отримання сторінки

    # код для отримання необхідних даних

    random_number = random.randint(5, 10)
    await asyncio.sleep(random_number)

    # збереження даних у Redis
    r.set('my_key', random_number)

    save_cookies_to_file(driver, 'cooc_as')
    driver.quit()  # закриття драйвера


async def main():
    semaphore = asyncio.Semaphore(5)
    tasks = []
    for url in urls:
        await semaphore.acquire()
        task = asyncio.ensure_future(parse_page(url))
        task.add_done_callback(lambda x: semaphore.release())
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f'Time taken: {end - start} seconds')
