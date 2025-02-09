import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import functools

def fibon(n):
    if n < 2:
        return n

    return fibon(n-1) + fibon(n-2)

def fibon_worker(n):
    return n, fibon(n)

if __name__ == '__main__':
    # start = time.time()
    # for i in range(35):
    #     print(i, fibon(i))
    # stop = time.time()
    # print("Time taken in seconds: ", stop-start)

    start = time.time()
    with ProcessPoolExecutor() as executor:
        reuslts = [executor.submit(fibon_worker, i) for i in range(35, 0, -1)]
        for f in as_completed(reuslts):
            print(f.result())
    stop = time.time()
    print("Time taken in seconds: ", stop-start)

