import requests, logging, datetime
import asyncio
import redis

import argparse

from options import MAX_CONCURRENT_TASKS as OPT_MAX_CONCURRENT_TASKS
from options import REQUEST_TIMEOUT, TIME_EXPIRE


async def my_coroutine(proxy, time_expire):
    if check_proxy(proxy):
        r.lpush('proxies', proxy)
        logging.info(f"{datetime.datetime.now()} // Proxy {proxy} is working!")
    else:
        logging.info(f"{datetime.datetime.now()} // Proxy {proxy} is not working!")

    r.expire('proxies', time_expire)


def check_proxy(proxy):
    try:
        response = requests.get('https://www.google.com', proxies={'https': proxy}, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


async def worker(queue):
    while True:
        coroutine = await queue.get()
        try:
            await coroutine
        except Exception as e:
            print(f"Exception in coroutine++: {e}")
        finally:
            queue.task_done()


async def main(filename, max_concurrent_tasks, time_expire):
    queue = asyncio.Queue()

    # Start worker tasks
    workers = []
    for i in range(max_concurrent_tasks):
        worker_task = asyncio.create_task(worker(queue))
        workers.append(worker_task)

    # Add tasks to queue
    filename = filename
    with open(filename, 'r') as f:
        lines = f.readlines()

        for line in lines:
            await queue.put(my_coroutine(line, time_expire))
    f.close()

    # Wait for all tasks to be completed
    await queue.join()

    # Cancel worker tasks
    for worker_task in workers:
        worker_task.cancel()


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
              "&  python3 sel_translate/main/proxy/proxy.py -free_proxy_txt 'free_proxy_test.txt' -max_concurrent_tasks 10 -time_expire 360"
    parser = argparse.ArgumentParser(description=descStr)
    parser.add_argument('-free_proxy_txt', dest='FreeProxyTxt', required=True)
    parser.add_argument('-max_concurrent_tasks', dest='MAX_CONCURRENT_TASKS', required=False)
    parser.add_argument('-time_expire', dest='TIME_EXPIRE', required=False)

    args = parser.parse_args()

    free_proxy_txt = args.FreeProxyTxt

    if args.MAX_CONCURRENT_TASKS:
        max_concurrent_tasks = int(args.MAX_CONCURRENT_TASKS)
    else:
        max_concurrent_tasks = OPT_MAX_CONCURRENT_TASKS

    if args.TIME_EXPIRE:
        time_expire = int(args.TIME_EXPIRE)
    else:
        time_expire = TIME_EXPIRE

    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()

    logging.basicConfig(filename='proxy.log', encoding='utf-8', datefmt='%Y-%m-%d_%H-%M-%S', level=logging.INFO)
    asyncio.run(main(free_proxy_txt, max_concurrent_tasks, time_expire))

    print_proxies()
