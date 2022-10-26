from typing import List

from supplier_api_tester.v2.models import TestResult
from supplier_api_tester.v2.tests import (
    AVAILABILITY_TEST,
    BOOKING_TEST,
    PRODUCT_CATALOG,
    RESERVATION_TEST,
)


class SupplierApiTester(object):
    def __init__(
        self,
        host: str,
        api_key: str,
        product_id: str,
        test_target: str,
    ):
        self.host = host
        self.api_key = api_key
        self.product_id = product_id
        self.test_target = test_target

    def run(self) -> List[TestResult]:
        test_targets = {
            'availability': _run_tests(AVAILABILITY_TEST, self.host, self.api_key, self.product_id, 2),
            'reservation': _run_tests(RESERVATION_TEST, self.host, self.api_key, self.product_id, 2),
            'booking': _run_tests(BOOKING_TEST, self.host, self.api_key, self.product_id, 2),
            'catalog': _run_tests(PRODUCT_CATALOG, self.host, self.api_key, 2),
        }
        return list(test_targets[self.test_target])


def _run_tests(target, *args):
    return (test(*args) for test in target)
