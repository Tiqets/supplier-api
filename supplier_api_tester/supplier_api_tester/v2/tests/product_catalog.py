# If multiple checks can be done using the same response
# then they should be done under a single test case.

from supplier_api_tester.v2.decorators import test_wrapper
from supplier_api_tester.v2.models import TestResult
from ..utils.catalog import get_catalog


@test_wrapper
def test_get_products(api_url, api_key, version=2) -> TestResult:
    """Get product catalog"""
    _, products = get_catalog(api_url, api_key, version)
    for p in products:
        if p.required_visitor_data or p.required_order_data:
            return TestResult(
                status=1,
                message="Note that Tiqets will send the main booker’s name, email address and phone number with each reservation. Requiring ADDITIONAL customer data either at the order level (required_order_data ) and/or for each individual travel group member (required_visitor_data) should be done only if this is a hard requirement for the fulfillment or visitor entrance process."
            )
    return TestResult()
