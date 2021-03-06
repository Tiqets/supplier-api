import json
import requests
from requests.models import Response

from typing import Any, Callable, Tuple

from .exceptions import FailedTest


def client(
    url: str,
    api_key: str,
    params: dict = None,
    headers: dict = None,
    method: Callable = requests.get,
    json_payload=None,
) -> Tuple[Response, Any]:
    params = params if params is not None else {}
    headers = headers if headers is not None else {'API-Key': api_key}
    try:
        response = method(url, params=params, headers=headers, json=json_payload)
    except requests.exceptions.ConnectionError:
        raise FailedTest(
            message=f'Connection error occured while testing endpoint {url}. Check if your server is available.',
            response=response,
        )
    except requests.exceptions.HTTPError:
        raise FailedTest(
            message=f'HTTP error occured while testing endpoint {url}',
            response=response,
        )

    if response.status_code not in (200, 204, 400, 403, 405, 500):
        raise FailedTest(
            message=f'Unexpected status code {response.status_code} from {url}',
            response=response,
        )

    if response.status_code in (204, 403, 405, 500):
        return response, None

    try:
        return response, response.json()
    except json.JSONDecodeError:
        raise FailedTest(
            message=f'Failed to decode JSON',
            response=response,
        )
