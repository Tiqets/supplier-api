# If multiple checks can be done using the same response
# then they should be done under a single test case.

from typing import List
from requests.models import Response

from supplier_api_tester.v2.decorators import test_wrapper
from supplier_api_tester.v2.exceptions import FailedTest
from supplier_api_tester.v2.models import Product, TestResult
from ..utils.catalog import get_catalog


@test_wrapper
def test_get_products(api_url, api_key, version=2):
    """Get product catalog"""
    get_catalog(api_url, api_key, version)
    return TestResult()


def _validate_timeslots(raw_response: Response, products: List[Product], use_timeslots: bool):
    for product in products:
        if product.use_timeslots != use_timeslots:
            raise FailedTest(
                message=f'Product {product.id} with non matching use_timeslots returned',
                response=raw_response,
            )
