# if path.isfile(DataFile):
#     file_with_data = open(DataFile, "rt")
#     words_count_sort = fill_words_count_from_file(file_with_data, lower_word=False)
#
#     path_to_file_result = OutputFile
#
#     save_data_to_file(words_count_sort, path_to_file_result, div)
#
#     file_with_data.close()
#     print(f'Ok')
# else:
#     print(f'file not exist')

# while True:
#     # отримуємо перший елемент зі списку та видаляємо його
#     proxy = r.lpop('proxies')
#     # print(proxy)
#     if proxy is None:
#         break
#     print(proxy.decode())
# sudo chmod 777 sel_translate/main/proxy/proxy.log
# import redis
# import logging, datetime
# def print_proxies():
#     l = []
#     r = redis.Redis(host='localhost', port=6379, db=0)
#     while True:
#         proxy = r.lpop('proxies')
#         l.append(proxy)
#         if proxy is None:
#             break
#     print(l)
#
#
# if __name__ == '__main__':
#     # logging.basicConfig(
#     #     filename='proxy.log',
#     #     encoding='utf-8',
#     #     datefmt='%Y-%m-%d_%H-%M-%S',
#     #     level=logging.INFO,
#     #     format='%(asctime)s - %(levelname)s - %(message)s',
#     #     filemode='a'  # додати записи до файлу з логами, якщо він вже існує
#     # )
#     # logging.info(f"{datetime.datetime.now()} // Is working!")
#
#     print_proxies()

import multiprocessing, time
from selenium import webdriver


def scrape(url):
    driver = webdriver.Chrome()
    driver.get(url)
    page_source = driver.page_source
    time.sleep(5)
    driver.close()
    # do something with the page source



if __name__ == '__main__':
    urls = [
        'https://en.wikipedia.org/wiki/0',
        'https://en.wikipedia.org/wiki/1',
        'https://en.wikipedia.org/wiki/2',
        'https://en.wikipedia.org/wiki/3',
    ]

    processes = []
    for url in urls:
        p = multiprocessing.Process(target=scrape, args=(url,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()