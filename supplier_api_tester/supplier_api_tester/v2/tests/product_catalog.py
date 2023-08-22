# If multiple checks can be done using the same response
# then they should be done under a single test case.

from supplier_api_tester.v2.decorators import test_wrapper
from supplier_api_tester.v2.models import TestResult
from ..utils.catalog import get_catalog


@test_wrapper
def test_get_products(api_url, api_key, version=2) -> TestResult:
    """Get product catalog"""
    get_catalog(api_url, api_key, version)
    return TestResult()
