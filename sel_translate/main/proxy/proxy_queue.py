import asyncio
import requests
from tqdm.asyncio import tqdm_asyncio
import redis


def check_proxy(proxy):
    try:
        response = requests.get('https://www.google.com', proxies={'https': proxy}, timeout=2)
        if response.status_code == 200:
            return (True, proxy)
        else:
            return (False, proxy)
    except:
        return (False, proxy)


async def producer(queue):
    filename = 'free_proxy_test.txt'
    with open(filename, 'r') as f:
        lines = f.readlines()

        with tqdm_asyncio(total=len(lines)) as pbar:
            for line in lines:
                await queue.put(check_proxy(line))
                pbar.update(1)
    f.close()


async def consumer(queue):
    with tqdm_asyncio(total=queue.maxsize) as pbar:
        while True:

            item = await queue.get()
            await asyncio.sleep(2)  # імітуємо процес споживання
            r.lpush('proxies', str(item))
            queue.task_done()
            pbar.update(1)

            if queue.empty() and not queue._unfinished_tasks:
                break
    r.expire('proxies', 3600)


async def main():
    queue = asyncio.Queue(maxsize=5)
    tasks = []
    tasks.append(asyncio.create_task(producer(queue)))
    tasks.append(asyncio.create_task(consumer(queue)))
    await asyncio.gather(*tasks)
    await queue.join()


if __name__ == '__main__':
    # запуск асинхронної функції main()
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()

    asyncio.run(main())

    l = []
    while True:
        # отримуємо перший елемент зі списку та видаляємо його
        proxy = r.lpop('proxies')
        l.append(proxy)
        if proxy is None:
            break
    print(l)
