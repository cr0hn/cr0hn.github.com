import timeit
import aiohttp
import asyncio
import urllib.error
import urllib.request as req

from time import sleep
from multiprocessing import Pool
from threading import Thread, Semaphore


"""
Measure performance when download a lof of web pages
"""

CONCURRENCE = 0
URLS = 0

# --------------------------------------------------------------------------
# Download for threads
# --------------------------------------------------------------------------
def download_threads(url, sem_threads):
    try:
        response = req.urlopen(url)
        data = response.read()
    except urllib.error.URLError:
        print("Error in URL: ", url)
    sem_threads.release()


# --------------------------------------------------------------------------
# Threads
# --------------------------------------------------------------------------
def test_threads(concurrence, pages):

    sem_threads = Semaphore(concurrence)

    th = []
    th_append = th.append
    for page in pages:
        sem_threads.acquire()
        t = Thread(target=download_threads, args=(page, sem_threads))
        t.start()
        th_append(t)

    # Wait for threads ends
    map(Thread.join, th)


# --------------------------------------------------------------------------
# Processes
# --------------------------------------------------------------------------
def download_processes(url):
    try:
        response = req.urlopen(url)
        data = response.read()
    except urllib.error.URLError:
        print("Error in URL: ", url)


# ----------------------------------------------------------------------
def test_processes(concurrence, pages):
    mp = Pool(concurrence)
    mp.map(download_processes, pages)


# --------------------------------------------------------------------------
# Python 3 Coroutines
# --------------------------------------------------------------------------
@asyncio.coroutine
def download_coroutine(url, sem):
    conn = aiohttp.ProxyConnector(proxy=PROXY)
    with (yield from sem):
        response = yield from aiohttp.request('GET', url, connector=conn)
        data = (yield from response.read())


# ----------------------------------------------------------------------
def test_coroutines(concurrence, pages):
    sem_coroutines = asyncio.Semaphore(concurrence)

    f = asyncio.wait([download_coroutine(page, sem_coroutines) for page in pages])
    asyncio.get_event_loop().run_until_complete(f)

import urllib.request as req
PROXY = "http://172.31.219.30:8080"
hc = req.HTTPCookieProcessor()
proxy = req.ProxyHandler({'http': PROXY})
opener = req.build_opener(hc, proxy)
req.install_opener(opener)

# --------------------------------------------------------------------------
# Time it!
# --------------------------------------------------------------------------
if __name__ == '__main__':
    BASE_URL = "http://www.bing.com/search?q=%s&go=&qs=n&form=QBLH&filt=all&pq=hello&sc=8-1&sp=-1&sk=&cvid=3c6b1fd5cbe0456b8c2370b57dc7ad38"

    testing_cases = {
        "Python 3 coroutines": "test_coroutines",
        "Threads": "test_threads",
        "Processes": "test_processes",
    }

    print("[*] Starting test")
    for requests in [50, 100, 200]:
        print(" " * 3, "- Requesting %s URLs:" % requests)

        for concurrence in [5, 10, 15]:
            print(" " * 5, "+ concurrence %s:" % concurrence)

            CONCURRENCE = concurrence
            URLS = [BASE_URL % w for w in range(requests)]

            for case_name, case_function in testing_cases.items():
                print(" " * 8, "> ", case_name,  "time: ",
                      timeit.timeit("%s(CONCURRENCE, URLS)" % case_function, setup="from __main__ import %s, CONCURRENCE, URLS" % case_function, number=1),
                      "seconds")
                sleep(1)

    print("[*] Tests end")