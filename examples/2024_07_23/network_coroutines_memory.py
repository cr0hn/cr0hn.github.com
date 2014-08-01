import time
import timeit
import aiohttp
import asyncio
import urllib.error
import memory_profiler
import urllib.request as req

from time import sleep
from multiprocessing import Pool
from threading import Thread, Semaphore
from random import randint


"""
Measure performance when download a lof of web pages
"""

CONCURRENCE = 0
URLS = 0


# --------------------------------------------------------------------------
# Download for threads
# --------------------------------------------------------------------------
# @memory_profiler.profile
def download_threads(url, sem_threads):
    try:
        response = req.urlopen(url)
        data = response.read()
    except urllib.error.URLError:
        print("Thread error in URL: ", url)
    sem_threads.release()


# --------------------------------------------------------------------------
# Threads
# --------------------------------------------------------------------------
@memory_profiler.profile
def test_threads():

    sem_threads = Semaphore(CONCURRENCE)

    th = []
    th_append = th.append
    for page in URLS:
        sem_threads.acquire()
        t = Thread(target=download_threads, args=(page, sem_threads))
        t.start()
        th_append(t)

    # Wait for threads ends
    for x in th:
        x.join()


# --------------------------------------------------------------------------
# Processes
# --------------------------------------------------------------------------
# @memory_profiler.profile
def download_processes(url):
    try:
        response = req.urlopen(url, )
        data = response.read()
    except urllib.error.URLError:
        print("Process Error in URL: ", url)


# ----------------------------------------------------------------------
@memory_profiler.profile
def test_processes():
    mp = Pool(CONCURRENCE)
    mp.map(download_processes, URLS)


# --------------------------------------------------------------------------
# Python 3 Coroutines
# --------------------------------------------------------------------------
@asyncio.coroutine
# @memory_profiler.profile
def download_coroutine(url, sem_coroutines):
    # conn = aiohttp.ProxyConnector(proxy=PROXY)
    with (yield from sem_coroutines):
        # response = yield from aiohttp.request('GET', url, connector=conn)
        response = yield from aiohttp.request('GET', url)
        data = (yield from response.read())
        # asyncio.sleep(0.01)
    # response = yield from aiohttp.request('GET', url, compress=True)
    # data = (yield from response.read())

    # response = yield from aiohttp.request('GET', url)
    # data = (yield from response.read())


# ----------------------------------------------------------------------
@memory_profiler.profile
def test_coroutines():
    sem_coroutines = asyncio.Semaphore(CONCURRENCE)

    f = asyncio.wait([download_coroutine(page, sem_coroutines) for page in URLS])
    asyncio.get_event_loop().run_until_complete(f)

# import urllib.request as req
# PROXY = "http://172.31.219.30:8080"
# hc = req.HTTPCookieProcessor()
# proxy = req.ProxyHandler({'http': PROXY})
# opener = req.build_opener(hc, proxy)
# req.install_opener(opener)

# --------------------------------------------------------------------------
# Time it!
# --------------------------------------------------------------------------
if __name__ == '__main__':
    testing_cases = {
        "Python 3 coroutines": "test_coroutines",
        "Threads": "test_threads",
        # "Processes": "test_processes",
    }

    print("[*] Starting test")
    # for requests in [50, 100]:
    for requests in [50]:

        BASE_URL = {
            'small': ['https://www.google.es/webhp?tab=ww&ei=AtXPU_ivMuyR1AWivIGIDg&ved=0CBAQ1S4#q=%s' % w for w in range(requests)],
            # 'middle': ['http://upload.wikimedia.org/wikipedia/commons/3/37/African_Bush_Elephant.jpg' for w in range(requests)],
            # 'heavy': ['http://cdimage.debian.org/debian-cd/7.6.0/amd64/iso-cd/debian-7.6.0-amd64-netinst.iso' for w in range(requests)]
        }

        print(" " * 3, "- Requesting %s URLs:" % requests)

        for i, concurrence in enumerate([5, 15]):
            CONCURRENCE = concurrence

            print(" " * 5, "+ concurrence %s:" % CONCURRENCE)

            for base_url_name, base_url in BASE_URL.items():
                URLS = base_url
                print(" " * 8, "file size:", base_url_name)
                for case_name, case_function in testing_cases.items():
                    # print(case_function)
                    start = time.time()
                    # p = memory_profiler.memory_usage((globals()["%s" % case_function], (), {}))
                    p = memory_profiler.memory_usage(globals()["%s" % case_function], retval=True, stream=None)
                    # print(p)

                    # print(globals()["%s" % case_function]())
                    end = time.time()

                    # print(end - start)
                    # p = memory_profiler.memory_usage((globals()["%s" % case_function](),))
                    # print(p)
                    # print(" " * 10, "> ", case_name,  "time: ",
                    #       timeit.timeit("%s()" % case_function, setup="from __main__ import %s" % case_function, number=1),
                    #       "seconds")

    print("[*] Tests end")