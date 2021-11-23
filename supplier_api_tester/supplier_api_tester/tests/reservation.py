from datetime import datetime, timedelta, timezone
from typing import Union

import requests

from ..client import client
from ..decorators import test_wrapper
from ..exceptions import FailedTest
from ..models import TestResult, Timeslot, ApiError
from ..utils.adapters import get_api_error
from ..utils.date import get_tomorrow
from ..utils.adapters import get_reservation
from ..utils.errors import check_api_error
from ..utils.reservation import get_payload_from_slot, get_reservation_slot


@test_wrapper
def test_missing_api_key(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Request without API-Key'''
    raw_response, _ = client(f'{api_url}/v{version}/products/{product_id}/reservation', api_key, method=requests.post, json_payload={}, headers={})

    if raw_response.status_code != 403:
        raise FailedTest(
            message=f'Incorrect status code "{raw_response.status_code}" when calling the API wihout the API-Key. Expected status code: "403".',
            response=raw_response,
        )

    if raw_response.text != 'Forbidden - Missing or incorrect API key':
        return TestResult(
            status=1,
            message=(
                f'Incorrect text message "{raw_response.text}". '
                'Expected message: "Forbidden - Missing or incorrect API key".'
            )
        )

    return TestResult()


@test_wrapper
def test_incorrect_api_key(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Request with incorrect API-Key'''

    raw_response, _ = client(f'{api_url}/v{version}/products/{product_id}/reservation', api_key, method=requests.post, json_payload={}, headers={
        'API-Key': 'NON-EXISTING-API-KEY',
    })

    if raw_response.status_code != 403:
        raise FailedTest(
            message=f'Incorrect status code "{raw_response.status_code}" when calling the API wihout the API-Key. Expected status code: "403".',
            response=raw_response,
        )

    if raw_response.text != 'Forbidden - Missing or incorrect API key':
        return TestResult(
            status=1,
            message=(
                f'Incorrect text message "{raw_response.text}". '
                'Expected message: "Forbidden - Missing or incorrect API key".'
            )
        )

    return TestResult()


@test_wrapper
def test_missing_argument_error(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Testing missing argument errors'''
    tomorrow = get_tomorrow()
    warnings: List[str] = []
    slot = get_reservation_slot(api_url, api_key, product_id, timeslots)

    # payload is empty
    json_payload = {}
    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/reservation', api_key, method=requests.post, json_payload=json_payload)
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=1000,
        error='Missing argument',
        message='Required argument "date" was not found',
    )
    result = check_api_error(raw_response, api_error, expected_error)
    if result.is_warning:
        warnings.append(result.message)

    # no tickets
    json_payload['date'] = tomorrow.isoformat()
    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/reservation', api_key, method=requests.post, json_payload=json_payload)
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=1000,
        error='Missing argument',
        message='Required argument "tickets" was not found',
    )
    result = check_api_error(raw_response, api_error, expected_error)
    if result.is_warning:
        warnings.append(result.message)

    # no customer
    json_payload['tickets'] = [{
        'variant_id': slot.variants[0].id,
        'quantity': 1,
    }]
    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/reservation', api_key, method=requests.post, json_payload=json_payload)
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=1000,
        error='Missing argument',
        message='Required argument "customer" was not found',
    )
    result = check_api_error(raw_response, api_error, expected_error)
    if result.is_warning:
        warnings.append(result.message)

    if warnings:
        return TestResult(
            status=1,
            message='\n '.join(warnings)
        )
    return TestResult()


@test_wrapper
def test_error_for_non_existing_product(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Testing reservation for non-existing product'''
    url = f'{api_url}/v{version}/products/NON-EXISTING-PRODUCT-ID/reservation'
    slot = get_reservation_slot(api_url, api_key, product_id, timeslots)
    json_payload = get_payload_from_slot(slot)
    if timeslots:
        json_payload['timeslot'] = slot.start
    raw_response, response = client(url, api_key, method=requests.post, json_payload=json_payload)
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=1001,
        error='Missing product',
        message='Product with ID NON-EXISTING-PRODUCT-ID doesn\'t exist',
    )
    check_api_error(raw_response, api_error, expected_error)
    return TestResult()


@test_wrapper
def test_incorrect_date_format(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Testing reservation with incorrect date format'''
    url = f'{api_url}/v{version}/products/{product_id}/reservation'
    bad_date_format = '05/05/2020'
    slot = get_reservation_slot(api_url, api_key, product_id, timeslots)
    json_payload = get_payload_from_slot(slot)
    json_payload['date'] = bad_date_format
    if timeslots:
        json_payload['timeslot'] = slot.start
    raw_response, response = client(url, api_key, method=requests.post, json_payload=json_payload)
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=2000,
        error='Incorrect date format',
        message=f'Incorrect date format {bad_date_format}, please use the YYYY-MM-DD format',
    )
    check_api_error(raw_response, api_error, expected_error)
    return TestResult()


@test_wrapper
def test_past_date(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Testing reservation with past date'''
    url = f'{api_url}/v{version}/products/{product_id}/reservation'
    slot = get_reservation_slot(api_url, api_key, product_id, timeslots)
    json_payload = get_payload_from_slot(slot)
    yesterday = datetime.utcnow().date() - timedelta(days=1)
    json_payload['date'] = yesterday.isoformat()
    if timeslots:
        json_payload['timeslot'] = slot.start
    raw_response, response = client(url, api_key, method=requests.post, json_payload=json_payload)
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=2009,
        error='Incorrect date',
        message=f'Cannot use the past date',
    )
    check_api_error(raw_response, api_error, expected_error)
    return TestResult()


@test_wrapper
def test_not_allowed_method(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Testing methods that are not allowed'''
    url = f'{api_url}/v{version}/products/{product_id}/reservation'
    slot = get_reservation_slot(api_url, api_key, product_id, timeslots)
    json_payload = get_payload_from_slot(slot)
    if timeslots:
        json_payload['timeslot'] = slot.start
    for method in (requests.get, requests.put, requests.patch, requests.delete):
        raw_response, _ = client(url, api_key, method=method, json_payload=json_payload)
        status_code = getattr(raw_response, 'status_code', 200)
        if status_code != 405:
            raise FailedTest(
                message=f'Incorrect status code "{status_code}" when calling the API via method {method.__name__.upper()}. Expected status code: "405".',
                response=raw_response,
            )
    return TestResult()


@test_wrapper
def test_reservation(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Reserving tickets for at least 1 variant'''
    url = f'{api_url}/v{version}/products/{product_id}/reservation'
    slot = get_reservation_slot(api_url, api_key, product_id, timeslots)
    json_payload = get_payload_from_slot(slot)
    if timeslots:
        json_payload['timeslot'] = slot.start
    raw_response, response = client(url, api_key, method=requests.post, json_payload=json_payload)
    reservation = get_reservation(raw_response, response)
    if not reservation.reservation_id:
        raise FailedTest(
            message='No reservation ID found',
            response=raw_response,
        )
    if not reservation.expires_at.tzname():
        raise FailedTest(
            message='Expiration time should have the timezone.',
            response=raw_response,
        )
    if datetime.now(timezone.utc) + timedelta(minutes=14) > reservation.expires_at:
        raise FailedTest(
            message='Reservation should be held at least 15 minutes.',
            response=raw_response,
        )
    return TestResult()
