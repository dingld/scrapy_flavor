import os
import logging
from scrapy.dupefilters import RFPDupeFilter
from scrapy_flavor.clock import SimpleClock


request_aged = object()


class AgedDupefilter(RFPDupeFilter):

    def __init__(self, path=None, debug=False):
        self.file = None
        self.fingerprints = dict()
        self.logdupes = True
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        if path:
            self.file = open(os.path.join(path, 'requests.seen'), 'a+')
            self.file.seek(0)
            for line in self.file:
                fp, t = line.rstrip().split(',')
                self.fingerprints.update({fp: float(t)})
        self.clock = SimpleClock()

    def request_seen(self, request, spider=None):
        """
        False if fingerprint:
            1. Never seen.
            2. Seen but aged.
        """
        fp = self.request_fingerprint(request)
        aged_at = self.fingerprints.get(fp)
        if aged_at and aged_at > self.clock.right_now():
            return True
        self._update_fingerprint(fp, 0)

    def request_aged(self, request):
        age = request.meta.get('age', 0)
        if age > 0:
            age_at = self.clock.aged_at(age)
            self._update_fingerprint(request, age_at)
            for url in request.meta.get('redirect_urls', []):
                self._update_fingerprint(request.replace(url=url), age_at)

    def _update_fingerprint(self, request, aged_at):
        fp = request if isinstance(request, str) \
            else self.request_fingerprint(request)
        self.fingerprints[fp] = aged_at
        if self.file:
            line = '%(fp)s,%(t)s\n' % {'fp': fp, 't': aged_at}
            self.file.write(line)
