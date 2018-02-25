import threading
import logging
import requests
import random
import os

from lxml.html import fromstring, tostring

log = logging.getLogger(__name__)


class HTTPProxy:
    def __init__(self):
        # add your proxies here if you want...
        self.proxies = []

    def get(self, url):
        """
        A small wrapper on top of the Requests to enable the proxies option. Instead of passing
        it explicitly everywhere, we will be using this.
        """
        if self.proxies:
            return requests.get(url, timeout=60, proxies={
                'http': random.choice(self.proxies),
                'https': random.choice(self.proxies).replace('http', 'https')
            })
        else:
            return requests.get(url, timeout=60)


class Crawl(threading.Thread):
    def __init__(self, queue):
        self.lock = threading.Lock()
        self.queue = queue
        super(Crawl, self).__init__()

    def run(self):
        """Worker thread to crawl the titles of adult websites."""
        while True:
            self.lock.acquire()
            if not self.queue.empty():
                item = self.queue.get()
                self.parse(item)
            self.lock.release()

    def doc(self, resp):
        """Converting the response to the doc element"""
        return fromstring(resp)

    def parse(self, item):
        """Parse the web page content of xnxx."""
        try:
            resp = HTTPProxy().get(item)
            doc = self.doc(resp.content)
            links = doc.xpath('.//div[@class="thumb-under"]//a')

            # create data set for the titles.

            path = os.path.dirname(os.path.abspath(__file__))
            titles = []
            for link in links:
                titles.append(link.text_content().strip() + "\n")
            with open(path + "/data/titles.txt", "a+") as w:
                w.writelines(titles)
        except:
            pass
