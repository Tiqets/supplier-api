from datetime import datetime, timedelta, timezone
from typing import Union

import requests

from ..client import client
from ..decorators import test_wrapper
from ..exceptions import FailedTest
from ..models import TestResult, ApiError
from ..tests.product_catalog import get_catalog
from ..utils.adapters import get_reservation, get_booking, get_api_error, get_products
from ..utils.reservation import get_payload_from_slot, get_reservation_slot
from ..utils.errors import check_api_error


@test_wrapper
def test_missing_reservation_id(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Booking without the reservation ID'''
    url = f'{api_url}/v{version}/booking'
    raw_response, response = client(url, api_key, method=requests.post, json_payload={})
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=1000,
        error='Missing argument',
        message='Required argument "reservation_id" was not found',
    )
    check_api_error(raw_response, api_error, expected_error)
    return TestResult()


@test_wrapper
def test_missing_api_key(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Booking without the API key'''
    url = f'{api_url}/v{version}/booking'
    raw_response, _ = client(url, api_key, method=requests.post, json_payload={}, headers={})

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
    '''Booking with incorrect API-Key'''
    url = f'{api_url}/v{version}/booking'
    raw_response, _ = client(url, api_key, method=requests.post, json_payload={}, headers={'API-Key': 'NON-EXISTING-API-KEY'})

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
def test_not_allowed_method(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Testing methods that are not allowed'''
    url = f'{api_url}/v{version}/booking'
    for method in (requests.get, requests.put, requests.patch, requests.delete):
        raw_response, _ = client(url, api_key, method=method, json_payload={})
        status_code = getattr(raw_response, 'status_code', 200)
        if status_code != 405:
            raise FailedTest(
                message=f'Incorrect status code "{status_code}" when calling the API via method {method.__name__.upper()}. Expected status code: "405".',
                response=raw_response,
            )
    return TestResult()


@test_wrapper
def test_booking_incorrect_reservation_id(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Booking with incorrect reservation ID.'''
    url = f'{api_url}/v{version}/booking'
    raw_response, response = client(url, api_key, method=requests.post, json_payload={
        'reservation_id': 'Tk9OLUVYSVNUSU5HLUlECg!!', # NON-EXISTING-ID
    })
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=3002,
        error='Incorrect reservation ID',
        message="Given reservation ID is incorrect",
    )
    check_api_error(raw_response, api_error, expected_error)
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
    raw_response, response = client(url, api_key, method=requests.post, json_payload=json_payload)
    reservation = get_reservation(raw_response, response)

    url = f'{api_url}/v{version}/booking'
    raw_response, response = client(url, api_key, method=requests.post, json_payload={
        'reservation_id': reservation.reservation_id,
        'order_reference': '12345678910',
    })
    booking = get_booking(raw_response, response)
    if booking.barcode_position == 'ticket':
        for variant_id, tickets_quantity in variant_quantity_map.items():
            tickets_for_variant = booking.tickets.get(variant_id)
            if tickets_for_variant is None:
                raise FailedTest(
                    message=f'No tickets for variant {variant_id}',
                    response=raw_response,
                )
            if len(tickets_for_variant) != tickets_quantity:
                raise FailedTest(
                    message=
                    f'Expected {tickets_quantity} codes for variant {variant_id} but got only {len(tickets_for_variant)}',
                    response=raw_response,
                )

    return TestResult()

@test_wrapper
def test_cancellation(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Perform booking that will be cancelled'''
    url = f'{api_url}/v{version}/products/{product_id}/reservation'
    slot = get_reservation_slot(api_url, api_key, product_id, timeslots)
    variant_quantity_map = {
         variant.id: 2 for variant in slot.variants if variant.max_tickets > 2
    }

    json_payload = get_payload_from_slot(slot, variant_quantity=2, min_quantity=3)
    if timeslots:
        json_payload['timeslot'] = slot.start
    raw_response, response = client(url, api_key, method=requests.post, json_payload=json_payload)
    reservation = get_reservation(raw_response, response)

    url = f'{api_url}/v{version}/booking'
    raw_response, response = client(url, api_key, method=requests.post, json_payload={
        'reservation_id': reservation.reservation_id,
    })
    booking = get_booking(raw_response, response)
    booking_id = booking.booking_id

    # check if product supports cancellations
    _, products = get_catalog(api_url, api_key, version)
    product = [product for product in products if product.id == product_id][0]

    # cancel existing booking
    url = f'{api_url}/v{version}/booking/{booking_id}'
    raw_response, response = client(url, api_key, method=requests.delete, json_payload={"booking_id": booking_id})

    # throw error if product does not support cancellation
    if not product.is_refundable:
        api_error = get_api_error(raw_response, response)
        expected_error = ApiError(
            error_code=3004,
            error='Cancellation not possible',
            message='The booking cannot be cancelled, the product does not allow cancellations',
        )
        check_api_error(raw_response, api_error, expected_error)
        return TestResult(
            status=1,
            message=(
                "Skipping that test because the product does not support cancellations"
            )
        )

    # cancel booking in refundable product that cannot be cancelled due to cut_off time/being past date
    if product.use_timeslots:
        booking_for_time = datetime.fromisoformat(f'{slot.date.isoformat()} {slot.start}')
    else:
        booking_for_time = datetime.fromisoformat(slot.date.isoformat())
    cancellation_time = datetime.utcnow()
    if booking_for_time < cancellation_time:
        api_error = get_api_error(raw_response, response)
        expected_error = ApiError(
            error_code=2009,
            error='Incorrect date',
            message='Cannot use the past date',
        )
        check_api_error(raw_response, api_error, expected_error)

    difference = booking_for_time - cancellation_time
    hours_in_advance = round(difference.total_seconds()/3600)
    if product.cutoff_time != 0 and product.cutoff_time > hours_in_advance:
        api_error = get_api_error(raw_response, response)
        expected_error = ApiError(
            error_code=2009,
            error='Incorrect date',
            message=f'The booking can only be cancelled {product.cutoff_time} hours in advance',
        )
        check_api_error(raw_response, api_error, expected_error)

    # cancel booking that was already cancelled:
    url = f'{api_url}/v{version}/booking/{booking_id}'
    raw_response, response = client(url, api_key, method=requests.delete)

    cancel_date_ok = (booking_for_time > cancellation_time)
    cancelled_before_cutoff = (product.cutoff_time == 0 or product.cutoff_time < hours_in_advance)
    cancellation_time_ok = (cancel_date_ok and cancelled_before_cutoff)
    if cancellation_time_ok and product.is_refundable:
        api_error = get_api_error(raw_response, response)
        expected_error = ApiError(
            error_code=3003,
            error='Already cancelled',
            message=f'The booking with ID {booking_id} was already cancelled',
        )
        check_api_error(raw_response, api_error, expected_error)

    # cancel booking with no ID/non-existent ID
    non_existing_booking_id = "I-DO-NOT-EXIST"
    url = f'{api_url}/v{version}/booking/{non_existing_booking_id}'
    raw_response, response = client(url, api_key, method=requests.delete, json_payload={"booking_id": non_existing_booking_id})
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=1004,
        error='Missing booking',
        message=f"Booking with ID {booking_id} doesn't exist",
    )
    check_api_error(raw_response, api_error, expected_error)
    return TestResult()

