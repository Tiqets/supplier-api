import time
from functools import wraps

from .exceptions import FailedTest
from .models import TestResult
from .utils.conversions import ns_to_ms


def test_wrapper(f):
    '''
    This wrapper is doint 3 things:
      - creates the TestResult if the FailedTest exception occurs while running test function
      - adds the test tile from the test function docstring
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
            )
        test_result.title = f.__doc__
        test_result.duration = ns_to_ms(time.time_ns() - start)
        return test_result
    return decorated_function
