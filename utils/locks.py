from threading import Lock


class CountingLock:
    def __init__(self, n):
        self.n = n
        self.lock = Lock()

    def acquire_lock(self):
        while True:
            with self.lock:
                if self.n > 0:
                    self.n -= 1
                    return True

    def release_lock(self):
        with self.lock:
            self.n += 1
