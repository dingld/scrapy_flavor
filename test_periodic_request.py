import time
from scrapy import Request, Spider
from scrapy_flavor.decorators import every, config


class ExampleSpider(Spider):

    name = 'bing'

    custom_settings = dict(
        CLOSESPIDER_TIMEOUT=60*30,
        CONCURRENT_REQUESTS_PER_DOMAIN=1,
        DUPEFILTER_DEBUG=True,
        HTTPCACHE_ENABLED=True,
        HTTPCACHE_DIR='/tmp',
        HTTPCACHE_EXPIRATION_SECS=60 * 60 * 24,
        EXTENSIONS={'scrapy_flavor.periodic.StartRequests': 1},
        JOBDIR='/tmp/%s' % name,
        LOG_FORMAT='%(asctime)s.%(msecs)03d [%(name)s] %(levelname)s: %(message)s',
        LOG_LEVEL='DEBUG',
        REDIRECT_ENABLED=False,
        RETRY_ENABLED=False,
        ROBOTSTXT_OBEY=True,
        USER_AGENT=('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'),
    )

    @every(age=1)
    def start_requests(self):
        meta = {'dont_obey_robotstxt': True}
        for url in self.start_urls:
            yield Request(url, meta=meta, callback=self.index_page)

    @config(age=10)
    def index_page(self, response):
        for href in response.css('#b_results > li h2 a::attr(href)'):
            yield response.follow(href, callback=self.detail_page)

    @config(age=60, priority=3)
    def detail_page(self, response):
        return {
            'scraped_at': time.time(),
            'url': response.url,
            'title': (response.css('title::text').extract_first() or '').strip(),
        }


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    start_urls = ['https://www.bing.com/search?q=linux']
    process.crawl(ExampleSpider, start_urls=start_urls)
    process.start()