from flask import request

from functools import wraps

from . import exceptions, utils


def date_range_validator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start = utils.get_date(request.args, 'start')
        end = utils.get_date(request.args, 'end')
        if start > end:
            raise exceptions.BadRequest(2001, 'Incorrect date range', 'The end date cannot be earlier than start date')
        return f(*args, **kwargs)
    return decorated_function
