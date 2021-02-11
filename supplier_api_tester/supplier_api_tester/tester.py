from typing import List

from .models import TestResult
from .tests import (
    AVAILABILITY_TEST,
    AVAILABILITY_VARIANTS_TEST,
    AVAILABILITY_TIMESLOTS_TEST,
    BOOKING_TEST,
    PRODUCT_CATALOG,
    RESERVATION_TEST,
)
from .utils.reservation import get_reservation_slot


class SupplierApiTester(object):

    def __init__(
        self,
        host: str,
        api_key: str,
        product_id: str,
        test_target: str,
        timeslots: bool,
    ):
        self.host = host
        self.api_key = api_key
        self.product_id = product_id
        self.test_target = test_target
        self.timeslots = timeslots

    def run(self) -> List[TestResult]:
        TEST_TARGETS = {
            'availability': _run_tests(AVAILABILITY_TEST, self.host, self.api_key, self.product_id),
            'reservation': _run_tests(RESERVATION_TEST, self.host, self.api_key, self.product_id, self.timeslots),
            'booking': _run_tests(BOOKING_TEST, self.host, self.api_key, self.product_id, self.timeslots),
            'catalog': _run_tests(PRODUCT_CATALOG, self.host, self.api_key),
            'timeslots': _run_tests(AVAILABILITY_TIMESLOTS_TEST, self.host, self.api_key, self.product_id),
            'variants': _run_tests(AVAILABILITY_VARIANTS_TEST, self.host, self.api_key, self.product_id),
        }
        results = list(TEST_TARGETS[self.test_target])
        if self.test_target == 'availability':
            if self.timeslots:
                return results + list(TEST_TARGETS['timeslots'])
            else:
                return results + list(TEST_TARGETS['variants'])
        return results


def _run_tests(target, *args):
    return (test(*args) for test in target)
