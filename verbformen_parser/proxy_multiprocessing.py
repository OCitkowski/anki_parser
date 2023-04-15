# run
# python3 verbformen_parser/proxy_multiprocessing.py -free_proxy_txt 'verbformen_parser/free_proxy.txt' -max_concurrent_tasks 25


import requests, logging, multiprocessing, datetime
import redis
import argparse

from settings import MAX_CONCURRENT_TASKS as OPT_MAX_CONCURRENT_TASKS
from settings import REQUEST_TIMEOUT, NAME_REDIS_PROXY


def get_proxis_from_txt(filename):
    proxies = []
    try:

        with open(filename, 'r') as f:
            lines = f.readlines()

            for line in lines:
                proxies.append(line)
    except Exception as e:
        pass
    finally:
        f.close()
    return proxies


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


def main(proxy):
    result = check_proxy(proxy)
    r = redis.Redis(host='localhost', port=6379, db=0)

    if result and proxy.rstrip('\n') != None and proxy.rstrip('\n') != '':
        print(f"{proxy}:work {result}")

        r.lpush(NAME_REDIS_PROXY, proxy.rstrip('\n'))
        logging.info(f"{datetime.datetime.now()} // Proxy {proxy} is working!")
    else:
        print(f"{proxy}:does not work")




def print_proxies():
    # l = []
    # while True:
    #     proxy = r.lpop(NAME_REDIS_PROXY)
    #     l.append(proxy)
    #     if proxy is None:
    #         break
    # print(l)
    r = redis.Redis(host='localhost', port=6379, db=0)
    items = r.lrange(NAME_REDIS_PROXY, 0, -1)
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
        max_concurrent_tasks = OPT_MAX_CONCURRENT_TASKS

    r = redis.Redis(host='localhost', port=6379, db=0)
    # r.flushdb()

    proxies = get_proxis_from_txt(free_proxy_txt)

    with multiprocessing.Pool(processes=max_concurrent_tasks) as pool:
        pool.map(main, proxies)

    r.expire(NAME_REDIS_PROXY, 3600)

    print_proxies()
