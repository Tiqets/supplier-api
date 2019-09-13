from supplier_api_tester.exceptions import FailedTest
from supplier_api_tester.models import TestResult


def check_api_error(api_error, expected_error) -> TestResult:
    '''Chcking if the API error matches the expected error'''
    if api_error.error_code != expected_error.error_code:
        raise FailedTest(f'Incorrect error_code ({api_error.error_code}). Expected value: {expected_error.error_code}')
    if api_error.error != expected_error.error:
        raise FailedTest(f'Incorrect error text ({api_error.error}). Expected text: {expected_error.error}')
    if not api_error.message.startswith(expected_error.message):
        return TestResult(
            status=1,
            message=f'Incorrect message text ({api_error.message}). Expected text: {expected_error.message}',
        )
    return TestResult()
