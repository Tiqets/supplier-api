import json
import requests

from typing import Callable

from .exceptions import FailedTest


def client(
    url: str,
    api_key: str,
    params: dict = None,
    headers: dict = None,
    method: Callable = requests.get,
    json_payload=None,
):
    params = params if params is not None else {}
    headers = headers if headers is not None else {'API-Key': api_key}
    try:
        response = method(url, params=params, headers=headers, json=json_payload)
    except requests.exceptions.ConnectionError:
        raise FailedTest(
            message=f'Connection error occured while testing endpoint {url}. Check if your server is available.'
        )
    except requests.exceptions.HTTPError:
        raise FailedTest(message=f'HTTP error occured while testing endpoint {url}')

    if response.status_code not in (200, 400, 403, 405, 500):
        raise FailedTest(message=f'Unexpected status code {response.status_code} from {url}')

    if response.status_code in (403, 405, 500):
        return response

    try:
        return response.json()
    except json.JSONDecodeError:
        raise FailedTest(message=f'Response from the {url} was not in a JSON format')
