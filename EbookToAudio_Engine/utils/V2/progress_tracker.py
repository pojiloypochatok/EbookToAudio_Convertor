import threading


class ProgressTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self._progress = 0
        self._done = False
        self._error = None

    def set(self, value: int):
        with self._lock:
            self._progress = min(100, max(0, value))

    def get(self) -> int:
        with self._lock:
            return self._progress

    def mark_done(self):
        with self._lock:
            self._progress = 100
            self._done = True

    def set_error(self, error: Exception):
        with self._lock:
            self._error = error

    def is_done(self):
        with self._lock:
            return self._done

    def get_error(self):
        with self._lock:
            return self._error
