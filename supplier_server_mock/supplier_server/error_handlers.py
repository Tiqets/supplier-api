from flask import request


def bad_method(exception):
    return f'Method Not Allowed - Incorrect method was used ({request.method})', 405


def server_error(exception):
    return 'Service Error - Please report that', 500


def bad_request(exception):
    return {
        "error_code": exception.error_code,
        "error": exception.error,
        "message": exception.message,
    }, 400
