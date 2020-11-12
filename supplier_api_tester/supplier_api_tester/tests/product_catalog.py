import requests
from requests.models import Response

from ..client import client
from ..decorators import test_wrapper
from ..exceptions import FailedTest
from ..models import TestResult
from ..utils.adapters import get_products


@test_wrapper
def test_get_products(api_url, api_key, version=1):
    '''Get product catalog'''
    url = f'{api_url}/v{version}/products'
    raw_response, response = client(url, api_key, method=requests.get)
    get_products(raw_response, response)
    return TestResult()


@test_wrapper
def test_get_timeslots_products(api_url, api_key, version=1):
    '''Get product catalog with use_timeslots=True query filter'''

    url = f'{api_url}/v{version}/products'
    raw_response, response = client(url, api_key, method=requests.get, params={'use_timeslots':'True'})
    products = get_products(raw_response, response)
    _validate_timeslots(raw_response, products, use_timeslots=True)
    return TestResult()


@test_wrapper
def test_get_no_timeslots_products(api_url, api_key, version=1):
    '''Get product catalog with use_timeslots=False query filter'''

    url = f'{api_url}/v{version}/products'
    raw_response, response = client(url, api_key, method=requests.get, params={'use_timeslots':'False'})
    products = get_products(raw_response, response)
    _validate_timeslots(raw_response, products, use_timeslots=False)
    return TestResult()


def _validate_timeslots(raw_response: Response, products, use_timeslots):
    for product in products:
        if product.use_timeslots != use_timeslots:
            raise FailedTest(
                message=f'Product {product.id} with non matching use_timeslots returned',
                response=raw_response,
            )
