import json
import time
from functools import wraps

from .exceptions import FailedTest
from .models import TestResult, Response
from .utils.conversions import ns_to_ms


def test_wrapper(f):
    '''
    This wrapper is doing 3 things:
      - creates the TestResult if the FailedTest exception occurs while running test function
      - adds the test title from the test function docstring
      - measure the test duration in milliseconds
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start = time.time_ns()
        try:
            test_result = f(*args, **kwargs)
        except FailedTest as e:
            return TestResult(
                title=f.__doc__,
                status=2,
                message=e.message,
                duration=ns_to_ms(time.time_ns() - start),
                response=Response(
                    url=e.response.url,
                    status_code=e.response.status_code,
                    headers=e.response.headers,
                    payload=_format_json(e.response.request.body),
                    body=_format_json(e.response.text),
                ) if e.response is not None else None,
            )
        test_result.title = f.__doc__
        test_result.duration = ns_to_ms(time.time_ns() - start)
        return test_result
    return decorated_function


def _format_json(raw_data):
    if not raw_data:
        return None
    try:
        return json.dumps(json.loads(raw_data), indent=2)
    except:
        return raw_data
