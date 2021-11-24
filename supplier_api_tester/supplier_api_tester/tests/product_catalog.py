from typing import List, Optional, Tuple
import requests
from requests.models import Response

from ..client import client
from ..decorators import test_wrapper
from ..exceptions import FailedTest
from ..models import Product, TestResult
from ..utils.adapters import get_products


def get_catalog(
    api_url: str,
    api_key: str,
    version: int,
    use_timeslots: Optional[bool] = None,
) -> Tuple[Response, List[Product]]:
    url = f'{api_url}/v{version}/products'
    params = {}
    if use_timeslots is not None:
        params['use_timeslots'] = use_timeslots
    raw_response, response = client(url, api_key, method=requests.get, params=params)
    products = get_products(raw_response, response)
    return raw_response, products


@test_wrapper
def test_get_products(api_url, api_key, version=1):
    '''Get product catalog'''
    get_catalog(api_url, api_key, version)
    return TestResult()


@test_wrapper
def test_get_timeslots_products(api_url, api_key, version=1):
    '''Get product catalog with use_timeslots=True query filter'''
    raw_response, products = get_catalog(api_url, api_key, version, use_timeslots=True)
    _validate_timeslots(raw_response, products, use_timeslots=True)
    return TestResult()


@test_wrapper
def test_get_no_timeslots_products(api_url, api_key, version=1):
    '''Get product catalog with use_timeslots=False query filter'''
    raw_response, products = get_catalog(api_url, api_key, version, use_timeslots=False)
    _validate_timeslots(raw_response, products, use_timeslots=False)
    return TestResult()


def _validate_timeslots(raw_response: Response, products: List[Product], use_timeslots: bool):
    for product in products:
        if product.use_timeslots != use_timeslots:
            raise FailedTest(
                message=f'Product {product.id} with non matching use_timeslots returned',
                response=raw_response,
            )
