import time
from datetime import datetime, timedelta


class SimpleClock:

    def __init__(self):
        self.started_at = self.zero_clock()
        self.accuracy = 0.05

    def aged_at(self, age):
        if not age:
            return 0
        now = self.right_now()
        period = now - self.started_at
        error = period % age
        return now if self._skip(min(error, age-error)) else now - error + age

    def zero_clock(self):
        now = datetime.utcnow()
        return (now - datetime(1970, 1, 1)) / timedelta(seconds=1)

    def right_now(self):
        return time.time()

    def is_due(self, age):
        return self.aged_at(age) <= self.right_now()

    def _skip(self, error):
        return abs(error) <= self.accuracy
