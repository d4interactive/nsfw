import unittest
import logging
from queue import Queue

from nsfw.crawl import Crawl

logging.basicConfig(level=logging.INFO)


class TestCrawl(unittest.TestCase):
    def setUp(self):
        """Setting up the queue and passing the page URLs to crawl the data from."""
        self.queue_items = Queue()
        for i in range(1, 50):
            self.queue_items.put('http://www.xnxx.com/tags/18-porn/{0}'.format(i))
            self.queue_items.put('http://www.xnxx.com/tags/anal-fuck/{0}'.format(i))
            self.queue_items.put('http://www.xnxx.com/tags/anal/{0}'.format(i))
            self.queue_items.put('http://www.xnxx.com/tags/lesbian-porn/{0}'.format(i))
            self.queue_items.put('http://www.xnxx.com/tags/lesbian-sex/{0}'.format(i))
            self.queue_items.put('http://www.xnxx.com/tags/love/{0}'.format(i))
            self.queue_items.put('http://www.xnxx.com/tags/massage/{0}'.format(i))
            self.queue_items.put('http://www.xnxx.com/tags/massage-sex/{0}'.format(i))

    def test_xnxx(self):
        """Test case to crawl the titles from the XNXX.com"""
        for i in range(0, 10):
            c = Crawl(self.queue_items)
            c.run()


