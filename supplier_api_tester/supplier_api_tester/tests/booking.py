from datetime import datetime, timedelta, timezone
from typing import Union

import requests

from ..client import client
from ..decorators import test_wrapper
from ..exceptions import FailedTest
from ..models import TestResult, DailyAvailability, Timeslot, ApiError
from ..utils.adapters import get_reservation, get_booking, get_api_error
from ..utils.reservation import get_payload_from_slot, get_reservation_slot
from ..utils.errors import check_api_error


@test_wrapper
def test_missing_reservation_id(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Booking without the reservation ID'''
    url = f'{api_url}/v{version}/booking'
    response = client(url, api_key, method=requests.post, json_payload={})
    api_error = get_api_error(response)
    expected_error = ApiError(
        error_code=1000,
        error='Missing argument',
        message="Required argument end was not found",
    )
    check_api_error(api_error, expected_error)
    return TestResult()


@test_wrapper
def test_missing_api_key(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Booking without the API key'''
    url = f'{api_url}/v{version}/booking'
    response = client(url, api_key, method=requests.post, json_payload={}, headers={})

    if response.status_code != 403:
        raise FailedTest(
            f'Incorrect status code ({response.status_code}) when calling the API wihout the API-Key. '
            'Expected status code: 403.'
        )

    if response.text != 'Forbidden - Missing or incorrect API key':
        raise TestResult(
            status=1,
            message=(
                f'Incorrect text message ({response.text}). '
                'Expected message: Forbidden - Missing or incorrect API key'
            )
        )
    return TestResult()


@test_wrapper
def test_incorrect_api_key(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Booking with incorrect API-Key'''
    url = f'{api_url}/v{version}/booking'
    response = client(url, api_key, method=requests.post, json_payload={}, headers={'API-Key': 'NON-EXISTING-API-KEY'})

    if response.status_code != 403:
        raise FailedTest(
            f'Incorrect status code ({response.status_code}) when calling the API wihout the API-Key. '
            'Expected status code: 403.'
        )

    if response.text != 'Forbidden - Missing or incorrect API key':
        raise TestResult(
            status=1,
            message=(
                f'Incorrect text message ({response.text}). '
                'Expected message: Forbidden - Missing or incorrect API key'
            )
        )

    return TestResult()


@test_wrapper
def test_not_allowed_method(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Testing methods that are not allowed'''
    url = f'{api_url}/v{version}/booking'
    for method in (requests.get, requests.put, requests.patch, requests.delete):
        response = client(url, api_key, method=method, json_payload={})
        if response.status_code != 405:
            raise FailedTest(
                f'Incorrect status code ({response.status_code}) when calling the API via method {method}. '
                'Expected status code: 405.'
            )
    return TestResult()


@test_wrapper
def test_booking_incorrect_reservation_id(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Booking with incorrect reservation ID.'''
    url = f'{api_url}/v{version}/booking'
    response = client(url, api_key, method=requests.post, json_payload={
        'reservation_id': 'NON-EXISTING-ID',
    })
    api_error = get_api_error(response)
    expected_error = ApiError(
        error_code=3002,
        error='Incorrect reservation ID',
        message="Given reservation ID is incorrect",
    )
    check_api_error(api_error, expected_error)
    return TestResult()

@test_wrapper
def test_booking(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Booking tickets for at least 1 variant'''
    url = f'{api_url}/v{version}/products/{product_id}/reservation'
    slot = get_reservation_slot(api_url, api_key, product_id, timeslots)
    variant_quantity_map = {
         variant.id: 2 for variant in slot.variants if variant.max_tickets > 2
    }

    json_payload = get_payload_from_slot(slot, variant_quantity=2, min_quantity=3)
    if timeslots:
        json_payload['timeslot'] = slot.start
    response = client(url, api_key, method=requests.post, json_payload=json_payload)
    reservation = get_reservation(response)

    url = f'{api_url}/v{version}/booking'
    response = client(url, api_key, method=requests.post, json_payload={
        'reservation_id': reservation.reservation_id,
    })
    booking = get_booking(response)
    if booking.barcode_position == 'ticket':
        for variant_id, tickets_quantity in variant_quantity_map.items():
            tickets_for_variant = booking.tickets.get(variant_id)
            if tickets_for_variant is None:
                raise FailedTest(f'No tickets for variant {variant_id}')
            if len(tickets_for_variant) != tickets_quantity:
                raise FailedTest(f'Expected {tickets_quantity} codes for variant {variant_id} but got only {len(tickets_for_variant)}')

    return TestResult()
