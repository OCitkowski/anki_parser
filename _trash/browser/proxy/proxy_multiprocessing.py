import requests, logging, multiprocessing, datetime
import redis
import argparse

from options import MAX_CONCURRENT_TASKS as OPT_MAX_CONCURRENT_TASKS
from options import REQUEST_TIMEOUT


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

    if result and proxy.rstrip('\n') != None and proxy.rstrip('\n') != '':
        print(f"{proxy}:work {result}")
        r.lpush('proxies', proxy.rstrip('\n'))
        logging.info(f"{datetime.datetime.now()} // Proxy {proxy} is working!")
    else:
        print(f"{proxy}:does not work {result}")


def print_proxies():
    l = []
    while True:
        proxy = r.lpop('proxies')
        l.append(proxy)
        if proxy is None:
            break
    print(l)


if __name__ == '__main__':

    descStr = "For find real proxy " \
              "&  python3 sel_translate/main/proxy/proxy_multiprocessing.py -free_proxy_txt 'free_proxy_test.txt' -max_concurrent_tasks 10 -time_expire 360"
    parser = argparse.ArgumentParser(description=descStr)
    parser.add_argument('-free_proxy_txt', dest='FreeProxyTxt', required=True)
    parser.add_argument('-max_concurrent_tasks', dest='MAX_CONCURRENT_TASKS', required=False)

    args = parser.parse_args()

    free_proxy_txt = args.FreeProxyTxt

    if args.MAX_CONCURRENT_TASKS:
        max_concurrent_tasks = int(args.MAX_CONCURRENT_TASKS)
    else:
        max_concurrent_tasks = OPT_MAX_CONCURRENT_TASKS

    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()

    # logging.basicConfig(
    #     # filename='proxy.log',
    #     # encoding='utf-8',
    #     datefmt='%Y-%m-%d_%H-%M-%S',
    #     level=logging.INFO,
    #     format='%(asctime)s - %(levelname)s - %(message)s',
    #     # filemode='a',  # додати записи до файлу з логами, якщо він вже існує
    #     handlers=[
    #         logging.FileHandler('proxy3.log', mode='w', encoding='utf-8'),
    #         logging.StreamHandler()
    # ]
    # )
    # logging.info(f"{datetime.datetime.now()} // Is working!")

    proxies = get_proxis_from_txt(free_proxy_txt)

    with multiprocessing.Pool(processes=max_concurrent_tasks) as pool:
        pool.map(main, proxies)

    # print_proxies()
