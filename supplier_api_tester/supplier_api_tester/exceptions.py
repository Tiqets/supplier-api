class FailedTest(Exception):
    message: str = None

    def __init__(self, message: str):
        self.message = message
