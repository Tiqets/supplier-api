class BadRequest(Exception):
    error_code = None
    error = None
    message = None

    def __init__(self, error_code: int, error: str, message: str):
        self.error_code = error_code
        self.error = error
        self.message = message
