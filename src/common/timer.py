import time


class Timer():
    def __init__(self):
        self._process_time_1 = time.time()

    def set_time(self):
        self._process_time_0 = self._process_time_1
        self._process_time_1 = time.time()

    @property
    def process_time(self):
        try:
            return self._process_time_1 - self._process_time_0
        except Exception:
            return -1