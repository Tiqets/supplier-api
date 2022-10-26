from typing import List, Tuple
import requests
from requests.models import Response

from supplier_api_tester.v2.client import client
from supplier_api_tester.v2.models import Product
from ..utils.adapters import get_products


def get_catalog(
        api_url: str,
        api_key: str,
        version: int = 2,
) -> Tuple[Response, List[Product]]:
    url = f'{api_url}/v{version}/products'
    raw_response, response = client(url, api_key, method=requests.get, params={})
    products = get_products(raw_response, response)
    return raw_response, products
