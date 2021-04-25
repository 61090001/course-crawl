from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib3
import logger

log = logger.get_logger(__name__)

http = urllib3.PoolManager()

class Crawler:

    def __init__(self, url, parser, max_depth=3, pool=None):
        self.url = url
        self.parser = parser
        self.max_depth = max_depth
        self.pool = pool
        if not self.pool:
            self.pool = dict()
        self.crawled_data = []
    
    def get_crawled_data(self):
        return self.crawled_data
    
    def request(self, url):
        try:
            r = http.request('GET', url)
            if r.status != 200:
                log.error(f"Request '{self.url}' error: {str(r.status)}")
                return
            return r.data.decode('utf-8')
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return

    def scrape(self, url):
        log.debug(f"Scraping {url}")
        html = self.request(url)
        if html is None:
            return
        
        parser = self.parser(html, self.pool)
        data = parser.extract()
        self.crawled_data.extend(data)
        urls = parser.get_follow_links()
        for url in urls:
            if self.max_depth > 1:
                url = urljoin(self.url, url)
                crawler = Crawler(url, self.parser, max_depth=self.max_depth-1, pool=self.pool)
                crawler.run()
                self.crawled_data.extend(crawler.get_crawled_data())
    
    def reset():
        self.pool = dict()
        self.crawled_data = []
    
    def run(self):
        self.scrape(self.url)
