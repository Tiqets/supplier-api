# If multiple checks can be done using the same response
# then they should be done under a single test case.

from typing import List
from typing import Set

from requests.models import Response

from supplier_api_tester.v2.decorators import test_wrapper
from supplier_api_tester.v2.exceptions import FailedTest
from supplier_api_tester.v2.models import Product, TestResult
from ..constants import PRODUCT_REQUIRED_ORDER_DATA_FIELDS
from ..constants import PRODUCT_REQUIRED_VISITOR_DATA_FIELDS
from ..utils.catalog import get_catalog


@test_wrapper
def test_get_products(api_url, api_key, version=2) -> TestResult:
    """Get product catalog"""
    get_catalog(api_url, api_key, version)
    return TestResult()


def _validate_required_order_data_fields(raw_response: Response, products: List[Product]) -> None:
    for product in products:
        if product.required_order_data:
            if not all([item.lower() in PRODUCT_REQUIRED_ORDER_DATA_FIELDS for item in product.required_order_data]):
                non_valid_fields: Set[str] = set(item.lower() for item in product.required_order_data).difference(
                    set(PRODUCT_REQUIRED_ORDER_DATA_FIELDS)
                )
                raise FailedTest(
                    message=(
                        f'Product {product.id} requires some non-valid additional, order-level fields: {non_valid_fields}.'
                    ),
                    response=raw_response,
                )


def _validate_required_visitor_data_fields(raw_response: Response, products: List[Product]) -> None:
    for product in products:
        if product.required_visitor_data:
            if not all(
                    [item.lower() in PRODUCT_REQUIRED_VISITOR_DATA_FIELDS for item in product.required_visitor_data]
            ):
                non_valid_fields: Set[str] = set(item.lower() for item in product.required_visitor_data).difference(
                    set(PRODUCT_REQUIRED_VISITOR_DATA_FIELDS)
                )
                raise FailedTest(
                    message=(
                        f'Product {product.id} requires some non-valid additional, visitor fields: {non_valid_fields}.'
                    ),
                    response=raw_response,
                )


@test_wrapper
def test_products_required_additional_fields(api_url, api_key, version=2) -> TestResult:
    """Products contain valid additional visitors and order-level fields."""
    response: Response
    products: List[Product]
    response, products = get_catalog(api_url, api_key, version)
    _validate_required_order_data_fields(response, products)
    _validate_required_visitor_data_fields(response, products)
    return TestResult()
