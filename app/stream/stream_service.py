import threading


class StreamService:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.frame = None

            cls._instance.lock = threading.Lock()

        return cls._instance

    def update(self, frame):

        with self.lock:

            self.frame = frame.copy()

    def get_frame(self):

        with self.lock:

            if self.frame is None:
                return None

            return self.frame.copy()