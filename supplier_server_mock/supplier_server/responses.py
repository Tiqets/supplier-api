def bad_request(error_code: int, error: str, message: str):
    return {
        "error_code": error_code,
        "error": error,
        "message": message,
    }, 400
