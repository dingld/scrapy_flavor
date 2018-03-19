from scrapy import signals


class ConfigurePriority:

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls()
        crawler.signals.connect(obj.request_scheduled, signals.request_scheduled)
        return obj

    def request_scheduled(self, request, spider):
        callback = request.callback or spider.parse
        priority = getattr(callback, '_priority', 0)
        request.priority = max(request.priority, priority)

