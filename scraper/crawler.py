from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urlparse, urljoin
import urllib3
import logger

log = logger.get_logger(__name__)

http = urllib3.PoolManager()

class Crawler:

    def __init__(self, urls, parser, max_depth=0, pool=None):
        self.urls = urls
        self.parser = parser
        self.max_depth = max_depth
        self.queue = deque()
        self.pool = pool
        if not self.pool:
            self.pool = dict()
        self.crawled_data = []
    
    def get_crawled_data(self):
        return self.crawled_data
    
    @staticmethod
    def request(url):
        try:
            r = http.request('GET', url)
            if r.status != 200:
                log.error(f"Request '{url}' error: {str(r.status)}")
                return
            return r.data.decode('utf-8')
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return

    def scrape(self, urls):
        self.queue.extend(urls)
        depth = self.max_depth
        levels = deque()
        counter = len(urls)

        while len(self.queue) > 0:
            url = self.queue.popleft()

            log.debug(f"Scraping {url}")
            html = Crawler.request(url)
            if html is None:
                continue

            parser = self.parser(html, self.pool)
            data = parser.extract()
            self.crawled_data.extend(data)
            if depth == 0:
                continue
            hyperlinks = parser.get_follow_links()
            levels.append(len(hyperlinks))
            for hyperlink in hyperlinks:
                self.queue.append(urljoin(url,hyperlink))
            counter -= 1
            if counter == 0:
                while len(levels) > 0:
                    counter += levels.popleft()
                depth -= 1
    
    def reset(self):
        self.queue = deque()
        self.pool = dict()
        self.crawled_data = []
    
    def run(self):
        self.reset()
        self.scrape(self.urls)
