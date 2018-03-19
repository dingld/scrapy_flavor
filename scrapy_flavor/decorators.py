from functools import wraps
from scrapy_flavor.periodic import request_aged


def every(age=60 * 5):
    """
    Crawl spider.start_requests every `age` seconds.
    """
    def wrap(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            self._every = age
            return func(self, *args, **kwargs)
        return wrapped
    return wrap


def config(age=60 * 60 * 24 * 30, priority=0):
    """
    Invalidate request fingerprint in `age` seconds.
    Set the request priority.
    """
    def wrap(func):
        @wraps(func)
        def wrapped(spider, response):
            func._priority = priority
            request = response.request
            request.meta.update(age=age)
            spider.crawler.signals.send_catch_log(request_aged, request=request)
            return func(spider, response)
        return wrapped
    return wrap
