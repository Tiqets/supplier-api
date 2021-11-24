from flask import request

from datetime import date, datetime, timedelta
from functools import wraps

import arrow

from . import constants, exceptions, utils


def date_range_validator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start = utils.get_date(request.args, 'start')
        end = utils.get_date(request.args, 'end')
        if start > end:
            raise exceptions.BadRequest(2001, 'Incorrect date range', 'The end date cannot be earlier than start date')
        if start < datetime.utcnow().date():
            raise exceptions.BadRequest(2009, 'Incorrect date', 'Cannot use the past date')
        if arrow.get(start).shift(months=constants.MAX_DATE_RANGE).date() < end:
            raise exceptions.BadRequest(
                2009,
                'Incorrect date',
                f'Maximum date range is {constants.MAX_DATE_RANGE} months'
            )
        return f(*args, **kwargs)
    return decorated_function
