---
title: "Python 3 AsyncIO vs threads vs procceses: Web content connections"
layout: post
---

# What is this post about?

This is the first of a serie of posts about the new Python 3.4 building library **AsyncIO**, in comparation of traditional Threads or Processes methods.

The purpose of this post series is to compare the performance, usability and advantages/disadvantes of each one solution.

Thoses are post that will be published:

1. **Web content connections**
2. Data base access
3. Slow taskes
4. Disc acceses


# Brief summary: Advantages and disadvantages of each method

The following table contains basic comparation between the three methods:

<table>
	<thead>
		<tr>
			<th>Method</th>
			<th>Advantages</th>
			<th>Disadvantages</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Threads</td>
			<td>
				<ul>
					<li>Secuencial flow of execution</li>
					<li>Simple programing way</li>
				</ul>
			</td>
			<td>
				<ul>
					<li>Not real multitasking</li>
					<li>Blocking mode</li>
					<li>Low performance</li>					
				</ul>
			</td>						
		</tr>		
		<tr>
			<td>Processes</td>
			<td>			
				<ul>
					<li>Real multiprocessing</li>
					<li>Secuencial flow execution</li>
					<li>Simple programing way</li>
				</ul>
			</td>
			<td>
				<ul>
					<li>Overload of system</li>
					<li>Not multithreads, instead use system processes</li>
				</ul>			
			</td>						
		</tr>
		<tr>
			<td>AsyncIO</td>
			<td>
				<ul>
					<li>Use [coroutines](http://en.wikipedia.org/wiki/Coroutine) to improve performance.</li>
					<li>Non-blocking based library</li>
					<li>Not overload the system</li>
				</ul>
			</td>
			<td>
				<ul>
					<li>Included only in Python 3.4.x</li>
					<li>Not linear programing</li>
				</ul>
			</td>						
		</tr>
	</tbody>
</table>


# Web content connections

The web content connections is one of the most blocking actions when we're developing. In these cases we can try to improve the performance using "multi-running" ways.

For the analysis, I was developed a 3 simple programs that uses Threads, Processes and coroutines.

## Testing method

For perform the test, I made a list of URLs of Bing search, generated in run time. Here is the code to do that:

{% highlight python lineno %}
# Global configs
MAX_CONCURRENCE = 10

# WEB_PAGES_PRELOADED = open("urls2.txt", "rU").readlines()
BASE_URL = "http://www.bing.com/search?q=%s&go=&qs=n&form=QBLH&filt=all&pq=hello&sc=8-1&sp=-1&sk=&cvid=3c6b1fd5cbe0456b8c2370b57dc7ad38"
WEB_PAGES_PRELOADED = [BASE_URL % x for x in range(150)]

{% endhighlight %}

 Analysis will check performance when combine maximum concurrent connections and number of URL.

All methods connections was limited to 15 concurrent.

Following the codes used for the testing (You can download entire source code in github: [source](http://github.com/cr0hn/blob/master/examples/2024_07_23/network_coroutines.py)):

## Threads code

{% highlight python %}
# --------------------------------------------------------------------------
# Download for threads
# --------------------------------------------------------------------------
def download_threads(url):
    try:
        response = req.urlopen(url)
        data = response.read()
    except urllib.error.URLError:
        print("Error in URL: ", url)
    sem_threads.release()

# --------------------------------------------------------------------------
# Threads
# --------------------------------------------------------------------------
sem_threads = Semaphore(MAX_CONCURRENCE)


# ----------------------------------------------------------------------
def test_threads():
    th = []
    th_append = th.append
    for page in WEB_PAGES_PRELOADED:
        sem_threads.acquire()
        t = Thread(target=download_threads, args=(page,))
        t.start()
        th_append(t)

    # Wait for threads ends
    map(Thread.join, th)
{% endhighlight %}

## Process code

{% highlight python %}
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
def test_processes():
    mp = Pool(MAX_CONCURRENCE)
    mp.map(download_processes, WEB_PAGES_PRELOADED)
{% endhighlight %}

# Tests method

The study will do some tasks, when are made concurrently, and compare execution results for these situations:

## Process code

{% highlight python %}
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
def test_processes():
    mp = Pool(MAX_CONCURRENCE)
    mp.map(download_processes, WEB_PAGES_PRELOADED)
{% endhighlight %}

## AsyncIO code

{% highlight python %}
# --------------------------------------------------------------------------
# Python 3 Coroutines
# --------------------------------------------------------------------------
sem_coroutines = asyncio.Semaphore(MAX_CONCURRENCE)

@asyncio.coroutine
def download_coroutine(url):
    response = yield from aiohttp.request('GET', url)
    data = (yield from response.read())


# ----------------------------------------------------------------------
def test_coroutines():
    f = asyncio.wait([download_coroutine(page) for page in WEB_PAGES_PRELOADED])
    asyncio.get_event_loop().run_until_complete(f)
{% endhighlight %}


# Results

Below you see the results of the excution. Source code used to perform the tests is [code](http://github.com/cr0hn/cr0hn.github.com/examples/network_coroutines.py)

{% highlight bash %}
cr0hn.com # python3.4 network_coroutines.py
[*] Starting test
    - Requesting 50 URLs:
      + concurrence 5:
         >  Threads time:  5.643185321998317 seconds
         >  Python 3 coroutines time:  6.230320422007935 seconds
         >  Processes time:  5.842057971982285 seconds
      + concurrence 10:
         >  Threads time:  2.679791122995084 seconds
         >  Python 3 coroutines time:  2.809677056997316 seconds
         >  Processes time:  3.4920346940052696 seconds
      + concurrence 15:
         >  Threads time:  1.9668658949958626 seconds
         >  Python 3 coroutines time:  2.065839316986967 seconds
         >  Processes time:  2.3969717799918726 seconds
    - Requesting 100 URLs:
      + concurrence 5:
         >  Threads time:  10.728528372012079 seconds
         >  Python 3 coroutines time:  10.180934254982276 seconds
         >  Processes time:  12.539949495985638 seconds
      + concurrence 10:
         >  Threads time:  6.375440713018179 seconds
         >  Python 3 coroutines time:  5.942036010994343 seconds
         >  Processes time:  6.644756149005843 seconds
      + concurrence 15:
         >  Threads time:  3.7005897909984924 seconds
         >  Python 3 coroutines time:  3.8714171170140617 seconds
         >  Processes time:  4.932254218001617 seconds
    - Requesting 200 URLs:
      + concurrence 5:
         >  Threads time:  21.58786587699433 seconds
         >  Python 3 coroutines time:  20.815504188009072 seconds
         >  Processes time:  23.112755888025276 seconds
      + concurrence 10:
         >  Threads time:  11.149541911989218 seconds
         >  Python 3 coroutines time:  10.273655647004489 seconds
         >  Processes time:  13.324604407011066 seconds
      + concurrence 15:
         >  Threads time:  7.853176967008039 seconds
         >  Python 3 coroutines time:  7.413613215001533 seconds
         >  Processes time:  9.253623016993515 seconds
[*] Tests end
{% endhighlight %}

Some gr