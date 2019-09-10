from .tests import (
    AVAILABILITY_TEST,
    AVAILABILITY_VARIANTS_TEST,
    AVAILABILITY_TIMESLOTS_TEST,
    RESERVATION_TEST,
    BOOKING_TEST,
)
from .utils.reservation import get_reservation_slot


class SupplierApiTester(object):

    def __init__(
        self,
        host: str,
        api_key: str,
        product_id: str,
        availability_test: bool,
        reservation_test: bool,
        booking_test: bool,
        timeslots: bool,
    ):
        self.host = host
        self.api_key = api_key
        self.product_id = product_id

        self.availability_test = availability_test
        self.reservation_test = reservation_test
        self.booking_test = booking_test
        self.timeslots = timeslots

    def run(self):
        if self.availability_test:
            results = [test(self.host, self.api_key, self.product_id) for test in AVAILABILITY_TEST]

            if self.timeslots:
                return results + [test(self.host, self.api_key, self.product_id) for test in AVAILABILITY_TIMESLOTS_TEST]
            else:
                return results + [test(self.host, self.api_key, self.product_id) for test in AVAILABILITY_VARIANTS_TEST]

        if self.reservation_test:
            return [test(self.host, self.api_key, self.product_id, self.timeslots) for test in RESERVATION_TEST]

        if self.booking_test:
            return [test(self.host, self.api_key, self.product_id, self.timeslots) for test in BOOKING_TEST]
