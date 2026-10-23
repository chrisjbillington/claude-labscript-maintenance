import time
from blacs.tab_base_classes import Worker


class TestWorker(Worker):
    def init(self):
        pass

    def sleep(self, delay):
        time.sleep(delay)
        return True
