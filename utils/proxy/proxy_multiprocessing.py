# run
# python3 verbformen_parser/proxy_multiprocessing.py -free_proxy_txt 'verbformen_parser/free_proxy.txt' -max_concurrent_tasks 25
import json
import re

import requests, multiprocessing
import redis
import argparse

from config.settings import MAX_CONCURRENT_TASKS
from config.settings import REQUEST_TIMEOUT, NAME_REDIS_PROXY, DB_PROXY_RADIS, PORT_PROXY_REDIS
import logging

# Створення об'єкта логування
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Створення обробника, який буде записувати логи в файл
handler = logging.FileHandler('verbformen_proxy.log')
handler.setLevel(logging.INFO)

# Створення форматувальника логів
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Додавання обробника до логера
logger.addHandler(handler)

redis_client = redis.Redis(host='localhost', port=PORT_PROXY_REDIS, db=DB_PROXY_RADIS)


def get_proxis_from_txt(filename, count_proxy: int = None):
    proxies = []
    try:

        with open(filename, 'r') as f:
            lines = f.readlines()

            for i, line in enumerate(lines):

                if count_proxy == None:
                    pass
                elif count_proxy - 1 < i:
                    break

                if line != None:
                    proxies.append(line.rstrip('\n'))

    except Exception as ex:
        logger.error(f'Failed / {ex}')

    finally:
        f.close()
    return proxies


def get_sorted_rating_proxy_list():
    rating_proxy_list = []
    keys = redis_client.keys()

    for key in keys:
        item_json = redis_client.get(key)
        rating_proxy_list.append(json.loads(item_json))

    # sorted_rating_proxy_list = sorted(rating_proxy_list, key=lambda item: item[1] - item[2], reverse=True)
    sorted_rating_proxy_list = sorted(rating_proxy_list, key=lambda x: (-x[1] + x[2], -x[1]))

    return sorted_rating_proxy_list


def failed_connect_proxy(new_proxy):
    try:
        response = requests.get('https://www.google.com', proxies={'https': new_proxy.rstrip('\n')},
                                timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            logger.info(f'Ok, check_proxy - {new_proxy}')
            return False
        else:
            return True
    except Exception as ex:
        logger.error(f'Failed / {ex}')

    return True


def get_key_proxy(proxy: str) -> 'key':
    return re.sub(r'\D', '', proxy)


def set_rating_proxy(new_proxy, key):
    # rating - [proxy, check_count, failed_connect_count]
    item = new_proxy.rstrip('\n')
    if item != None and item != '':
        rating_proxy = [item, 0, 0]
        item_proxy_json = json.dumps(rating_proxy)
        redis_client.set(key, item_proxy_json)
        logging.info(f"Key -{key} / Proxy - {new_proxy} set rating!")


def get_rating_proxy(key):
    rating_proxy = redis_client.get(key)
    if rating_proxy == None:
        return None
    else:
        return json.loads(rating_proxy.decode())


def update_rating_proxy(key, failed_connect=False):
    rating_proxy = get_rating_proxy(key)
    rating_proxy[1] += 1
    if failed_connect:
        rating_proxy[2] += 1  # failed_connect_count
    item_proxy_json = json.dumps(rating_proxy)
    redis_client.set(key, item_proxy_json)


def delete_rating_proxy_by_keys(keys: [list, str]):
    if isinstance(keys, list):
        for key in keys:
            redis_client.delete(key)
    elif isinstance(keys, str):
        redis_client.delete(keys)


def print_rating_proxy_s():
    keys = redis_client.keys()

    for key in keys:
        item_json = redis_client.get(key)
        print(json.loads(item_json))


def main(proxy):
    key = get_key_proxy(proxy)
    rating_proxy = get_rating_proxy(key)

    if rating_proxy == None:
        set_rating_proxy(proxy, key)
        rating_proxy = get_rating_proxy(key)

    update_rating_proxy(key, failed_connect_proxy(proxy))

    if rating_proxy[2] > 100:  # failed_connect_count
        delete_rating_proxy_by_keys(key)


def print_proxies():
    items = redis_client.lrange(NAME_REDIS_PROXY, 0, -1)
    for item in items:
        print('REDIS_PROXY-', item.decode())


if __name__ == '__main__':

    descStr = "For find real proxy " \
              "&  python3 verbformen_parser/proxy_multiprocessing.py -free_proxy_txt 'verbformen_parser/free_proxy.txt' -max_concurrent_tasks 25"
    parser = argparse.ArgumentParser(description=descStr)
    parser.add_argument('-free_proxy_txt', dest='FreeProxyTxt', required=False)
    parser.add_argument('-max_concurrent_tasks', dest='MAX_CONCURRENT_TASKS', required=False)

    args = parser.parse_args()

    free_proxy_txt = args.FreeProxyTxt

    if args.MAX_CONCURRENT_TASKS:
        max_concurrent_tasks = int(args.MAX_CONCURRENT_TASKS)
    else:
        max_concurrent_tasks = MAX_CONCURRENT_TASKS
    # # redis_client.flushdb()#

    # free_proxy_txt = 'free_proxy.txt'
    proxies = get_proxis_from_txt(free_proxy_txt, 1000)

    with multiprocessing.Pool(processes=MAX_CONCURRENT_TASKS) as pool:
        pool.map(main, proxies)

    for i, id in enumerate(get_sorted_rating_proxy_list()):
        print(i, id[0], id)
