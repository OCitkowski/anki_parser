import requests
import logging
import datetime
import asyncio
import random

from options import MAX_CONCURRENT_TASKS, REQUEST_TIMEOUT


async def my_coroutine(line):
    check_proxy(line)
    # await asyncio.sleep(random.uniform(0.0, 5.0))
    # print(f"Starting coroutine {line} ")


def check_proxy(proxy):
    print(proxy)
    try:

        response = requests.get('https://www.google.com', proxies={'https': proxy}, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:

            logging.info(f"{datetime.datetime.now()} // Proxy {proxy} is working!")

        else:
            logging.info(f"{datetime.datetime.now()} // Proxy {proxy} is not working!")

    except Exception as e:
        print(f"{e} -- Proxy {proxy} is not working!")


async def worker(queue):
    while True:
        coroutine = await queue.get()
        try:
            await coroutine
        except Exception as e:
            print(f"Exception in coroutine++: {e}")
        finally:
            queue.task_done()


async def main():
    queue = asyncio.Queue()

    # Start worker tasks
    workers = []
    for i in range(MAX_CONCURRENT_TASKS):
        worker_task = asyncio.create_task(worker(queue))
        workers.append(worker_task)

    # Add tasks to queue
    filename = 'free_proxy_test.txt'
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            await queue.put(my_coroutine(line))
    f.close()

    # Wait for all tasks to be completed
    await queue.join()

    # Cancel worker tasks
    for worker_task in workers:
        worker_task.cancel()


if __name__ == '__main__':
    logging.basicConfig(filename='proxy.log', encoding='utf-8', datefmt='%Y-%m-%d_%H-%M-%S', level=logging.INFO)
    asyncio.run(main())
