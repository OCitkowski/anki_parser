import multiprocessing
import time
from random import randint

def my_function(id):
    print(f"Starting process {id}")
    time.sleep(2)
    seconds = randint(1, 5)
    time.sleep(seconds)
    print(f"Ending process {id}")

def main():
    sem = multiprocessing.Semaphore(5)
    processes = []
    for i in range(20):
        p = multiprocessing.Process(target=my_function, args=(i,))
        processes.append(p)

    while processes:
        for p in processes:
            if p.is_alive():
                continue
            processes.remove(p)
            p.join()
            sem.release()

        while sem.acquire(block=False):
            if not processes:
                break
            p = processes.pop(0)
            p.start()

if __name__ == '__main__':
    main()
