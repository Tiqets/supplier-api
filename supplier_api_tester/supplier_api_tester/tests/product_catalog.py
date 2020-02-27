import requests

from ..client import client
from ..decorators import test_wrapper
from ..exceptions import FailedTest
from ..models import TestResult
from ..utils.adapters import get_products


@test_wrapper
def test_get_products(api_url, api_key, version=1):
    '''Get product catalog'''
    url = f'{api_url}/v{version}/products'
    response = client(url, api_key, method=requests.get)
    get_products(response)
    return TestResult()


@test_wrapper
def test_get_timeslots_products(api_url, api_key, version=1):
    '''Get product catalog with use_timeslots=true query filter'''

    url = f'{api_url}/v{version}/products'
    response = client(url, api_key, method=requests.get, params={'use_timeslot': True})
    products = get_products(response)
    _validate_timeslots(products, use_timeslots=True)
    return TestResult()


@test_wrapper
def test_get_no_timeslots_products(api_url, api_key, version=1):
    '''Get product catalog with use_timeslots=false query filter'''

    url = f'{api_url}/v{version}/products'
    response = client(url, api_key, method=requests.get, params={'use_timeslot': True})
    products = get_products(response)
    _validate_timeslots(products, use_timeslots=False)
    return TestResult()


def _validate_timeslots(products, use_timeslots):
    for product in products:
        if product.use_timeslot != use_timeslots:
            raise FailedTest(f'Product {product.id} with non matching use_timeslots returned')