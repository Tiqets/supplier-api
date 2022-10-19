from requests.models import Response


class FailedTest(Exception):
    message: str = None
    response: Response = None

    def __init__(self, message: str, response: Response = None):
        self.message = message
        self.response = response
