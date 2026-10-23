import time
from blacs.tab_base_classes import Worker


class TestWorker(Worker):
    def init(self):
        self.calls = 0

    def echo(self, value, delay=0):
        self.calls += 1
        time.sleep(delay)
        return value

    def count(self):
        return self.calls

    def fail(self):
        raise RuntimeError('deliberate worker failure')
