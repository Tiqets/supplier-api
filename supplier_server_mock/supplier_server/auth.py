from functools import wraps
from flask import request, Response


def authorization_header(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('API-Key')
        if not api_key or api_key != 'secret':
            return Response('Forbidden - Missing or incorrect API key', 403)
        return f(*args, **kwargs)
    return decorated_function
