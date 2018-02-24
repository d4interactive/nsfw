import threading
import logging
import requests
import random
import os

from lxml.html import fromstring, tostring

log = logging.getLogger(__name__)


class HTTPProxy:
    def __init__(self):
        self.proxies = PROXIES_LIST = [
            'http://contentstudio:fuckoff321@66.70.255.196:55887',
            'http://contentstudio:fuckoff321@142.44.249.192:55887',
            'http://contentstudio:fuckoff321@142.44.249.193:55887',
            'http://contentstudio:fuckoff321@142.44.249.194:55887',
            'http://contentstudio:fuckoff321@142.44.249.195:55887',
            'http://contentstudio:fuckoff321@142.44.249.196:55887',
            'http://contentstudio:fuckoff321@142.44.249.197:55887',
            'http://contentstudio:fuckoff321@142.44.249.198:55887',
            'http://contentstudio:fuckoff321@142.44.249.199:55887',
            'http://contentstudio:fuckoff321@142.44.249.200:55887',
            'http://contentstudio:fuckoff321@142.44.249.201:55887',
            'http://contentstudio:fuckoff321@142.44.249.202:55887',
            'http://contentstudio:fuckoff321@142.44.249.203:55887',
            'http://contentstudio:fuckoff321@142.44.249.204:55887',
            'http://contentstudio:fuckoff321@142.44.249.205:55887',
            'http://contentstudio:fuckoff321@142.44.249.206:55887',
            'http://contentstudio:fuckoff321@142.44.249.207:55887',
            'http://contentstudio:fuckoff321@142.44.249.208:55887',
            'http://contentstudio:fuckoff321@142.44.249.209:55887',
            'http://contentstudio:fuckoff321@142.44.249.210:55887',
            'http://contentstudio:fuckoff321@142.44.249.211:55887',
            'http://contentstudio:fuckoff321@142.44.249.212:55887',
            'http://contentstudio:fuckoff321@142.44.249.213:55887',
            'http://contentstudio:fuckoff321@142.44.249.214:55887',
            'http://contentstudio:fuckoff321@142.44.249.215:55887',
            'http://contentstudio:fuckoff321@142.44.249.216:55887',
            'http://contentstudio:fuckoff321@142.44.249.217:55887',
            'http://contentstudio:fuckoff321@142.44.249.218:55887',
            'http://contentstudio:fuckoff321@142.44.249.219:55887',
            'http://contentstudio:fuckoff321@142.44.249.220:55887',
            'http://contentstudio:fuckoff321@142.44.249.221:55887',
            'http://contentstudio:fuckoff321@142.44.249.222:55887',
            'http://contentstudio:fuckoff321@142.44.249.223:55887',
        ]

    def get(self, url):
        return requests.get(url, proxies={
            'http': random.choice(self.proxies),
            'https': random.choice(self.proxies).replace('http', 'https')
        })


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
        """Parse the web page content."""
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
