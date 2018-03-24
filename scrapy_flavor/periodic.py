from twisted.internet import task
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy_flavor.dupefilter import AgedDupeFilter, request_aged


class StartRequests:

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls()
        crawler.signals.connect(obj.dont_close, signals.spider_idle)
        crawler.signals.connect(obj.spider_opened, signals.spider_opened)
        return obj

    def start_requests(self, crawler):
        """
        Hack crawler.engine.slot to provide start_requests again
        """
        slot = crawler.engine.slot
        if slot and not slot.start_requests:
            slot.start_requests = iter(crawler.spider.start_requests())
            slot.nextcall.schedule()
            crawler.stats.inc_value('flavor/start_requests/beat', 1)

    def spider_opened(self, spider):
        """
        Hack crawler.engine.slot.scheduler to inject dupefilter with age
        """
        every = getattr(spider, '_every', 0)
        if every <= 0:
            return
        task.LoopingCall(self.start_requests, spider.crawler).start(every, now=False)
        spider.logger.info('Crawl spider.start_requests every %.3f seconds', every)
        scheduler = spider.crawler.engine.slot.scheduler
        spider.crawler.signals.connect(scheduler.df.request_aged, request_aged)

    def dont_close(self):
        raise DontCloseSpider