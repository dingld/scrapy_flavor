# scrapy_flavor
***Scrapy extensions*** to help periodic scraping, tiny change on code, similar configuration to pyspider's api.

### core module

- [X] `scrapy_flavor.periodic.StartRequests`: Schedule spider.start_requests periodically
- [X] `scrapy_flavor.dupefilter.AgedDupefilter`: Invalidate request fingerprint
- [X] `scrapy_flavor.priority.ConfigurePriority`: Adjust request priority

### decorator api

every(age)
- age: spider.start_request should be scheduled every age seconds.

config(age, piroirty)
- age: fingerprint of response should be invalidated in age seconds.
- priority: adjust priority to the request of this response

To enjoy the flavor, just ***decorate*** your spider together with ***extensions***
