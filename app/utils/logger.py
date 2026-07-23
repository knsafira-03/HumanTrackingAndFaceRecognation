from config import DEBUG


class Logger:

    @staticmethod
    def info(message):

        print(f"[INFO] {message}")

    @staticmethod
    def face(message):

        print(f"[FACE] {message}")

    @staticmethod
    def event(message):

        print(f"[EVENT] {message}")

    @staticmethod
    def database(message):

        print(f"[DATABASE] {message}")

    @staticmethod
    def warning(message):

        print(f"[WARNING] {message}")

    @staticmethod
    def error(message):

        print(f"[ERROR] {message}")

    @staticmethod
    def debug(message):

        if DEBUG:
            print(f"[DEBUG] {message}")