import asyncio
import random

from sel_translate.main.chrome_browser.browser_options import TOTAL_TASKS, MAX_CONCURRENT_TASKS

async def my_coroutine(id):
    print(f"Starting coroutine {id}")
    await asyncio.sleep(4)
    seconds = random.randint(1, 5)
    await asyncio.sleep(seconds)
    print(f"Ending coroutine {id}")

async def worker(queue):
    while True:
        coroutine = await queue.get()
        try:
            await coroutine
        except Exception as e:
            print(f"Exception in coroutine: {e}")
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
    for i in range(TOTAL_TASKS):
        await queue.put(my_coroutine(i))

    # Wait for all tasks to be completed
    await queue.join()

    # Cancel worker tasks
    for worker_task in workers:
        worker_task.cancel()

if __name__ == '__main__':
    asyncio.run(main())