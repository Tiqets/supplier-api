from datetime import date, datetime, timedelta

from typing import List, Tuple

import requests
from requests.models import Response

from supplier_api_tester.v2.client import client
from supplier_api_tester.v2.exceptions import FailedTest
from supplier_api_tester.v2.models import ApiError, DailyVariants, TestResult
from supplier_api_tester.v2.utils.adapters import (
    get_api_error,
    parse_availability_variants,
)
from supplier_api_tester.v2.utils.errors import check_api_error
from supplier_api_tester.v2.utils.date import get_tomorrow


def get_availability(
    api_url: str,
    api_key: str,
    product_id: str,
    version: int,
    start_date: date,
    end_date: date,
) -> Tuple[List[DailyVariants], Response]:
    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/availability', api_key, {
        'start': start_date.isoformat(),
        'end': end_date.isoformat(),
    })
    days: List[DailyVariants] = parse_availability_variants(raw_response, response)
    return days, raw_response


def past_start_date(api_url, api_key, product_id, endpoint, version=2):
    """Checking availability with start date from the past"""
    today = datetime.utcnow().date()
    start = today - timedelta(days=1)
    end = today

    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key, {
        'start': start.isoformat(),
        'end': end.isoformat(),
    })
    if not response:
        return TestResult()

    if start in response:
        raise FailedTest(
            message=f'Returned availability for date in the past: {start}',
            response=raw_response,
        )

    return TestResult()


def huge_date_range(api_url, api_key, product_id, endpoint, version=2):
    """Checking availability with huge date range"""
    today = datetime.utcnow().date()
    start = today
    end = today + timedelta(days=365 * 10)

    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key, {
        'start': start.isoformat(),
        'end': end.isoformat(),
    })
    return TestResult()


# TODO this no longer needed in v2 because the API error 2009 was removed. Check that the response is not 2009 error
def empty_availability(api_url, api_key, product_id, endpoint, version=2):
    """Checking availability that is supposed to be empty"""
    today = datetime.utcnow().date()
    start = today + timedelta(days=300)
    end = start + timedelta(days=1)

    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key, {
        'start': start.isoformat(),
        'end': end.isoformat(),
    })
    if not response:
        return TestResult()
    return TestResult(
        status=1,
        message=(
            "Skipping that test because response is not empty."
        )
    )


def test_missing_api_key(api_url, api_key, product_id, endpoint, version=2):
    """Request without API-Key"""
    tomorrow = get_tomorrow()
    raw_response, _ = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key, {
        'start': tomorrow.isoformat(),
        'end': tomorrow.isoformat(),
    }, headers={})
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


def test_incorrect_api_key(api_url, api_key, product_id, endpoint, version=2):
    """Request with incorrect API-Key"""
    tomorrow = get_tomorrow()
    raw_response, _ = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key, {
        'start': tomorrow.isoformat(),
        'end': tomorrow.isoformat(),
    }, headers={'API-Key': 'NON-EXISTING-API-KEY'})

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


def test_missing_argument_error(api_url, api_key, product_id, endpoint, version=2):
    """Testing missing argument errors"""
    tomorrow = get_tomorrow()
    warnings: List[str] = []

    # end is missing
    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key, {
        'start': tomorrow.isoformat(),
    })
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=1000,
        error='Missing argument',
        message='Required argument "end" was not found',
    )
    result = check_api_error(raw_response, api_error, expected_error)
    if result.is_warning:
        warnings.append(result.message)

    # start is missing
    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key, {
        'end': tomorrow.isoformat(),
    })
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=1000,
        error='Missing argument',
        message='Required argument "start" was not found',
    )
    result = check_api_error(raw_response, api_error, expected_error)
    if result.is_warning:
        warnings.append(result.message)

    # start and end are missing
    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key)
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=1000,
        error='Missing argument',
        message='Required argument "start" was not found',
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


def test_error_for_non_existing_product(api_url, api_key, product_id, endpoint, version=2):
    """Testing availability for non existing product"""
    tomorrow = get_tomorrow()
    raw_response, response = client(f'{api_url}/v{version}/products/NON-EXISTING-PRODUCT-ID/{endpoint}', api_key, {
        'start': tomorrow.isoformat(),
        'end': tomorrow.isoformat(),
    })
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=1001,
        error='Missing product',
        message='Product with ID NON-EXISTING-PRODUCT-ID doesn\'t exist',
    )
    return check_api_error(raw_response, api_error, expected_error)


def incorrect_date_format(api_url, api_key, product_id, endpoint, version=2):
    """Checking incorrect date format"""
    tomorrow = get_tomorrow()
    bad_date_format = tomorrow.strftime('%d-%m-%Y')

    # start date in a bad format
    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key, {
        'start': bad_date_format,
        'end': tomorrow.isoformat(),
    })
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=2000,
        error='Malformed datetime',
        message=f'Incorrect date format {bad_date_format}, please use the YYYY-MM-DD format',
    )
    check_api_error(raw_response, api_error, expected_error)

    # end date in a bad format
    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key, {
        'start': tomorrow.isoformat(),
        'end': bad_date_format,
    })
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=2000,
        error='Malformed datetime',
        message=f'Incorrect date format {bad_date_format}, please use the YYYY-MM-DD format',
    )
    check_api_error(raw_response, api_error, expected_error)

    return TestResult()


def end_before_start_error(api_url, api_key, product_id, endpoint, version=2):
    """Checking incorrect range error"""
    tomorrow = get_tomorrow()
    next_week = tomorrow + timedelta(days=7)
    raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key, {
        'start': next_week.isoformat(),
        'end': tomorrow.isoformat(),
    })
    api_error = get_api_error(raw_response, response)
    expected_error = ApiError(
        error_code=2001,
        error='Incorrect date range',
        message='The end date cannot be earlier than start date',
    )
    return check_api_error(raw_response, api_error, expected_error)


def not_allowed_method(api_url, api_key, product_id, endpoint, version=2):
    """Testing methods that are not allowed"""
    tomorrow = get_tomorrow()
    for method in (requests.post, requests.put, requests.patch, requests.delete):
        raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key, {
            'start': tomorrow.isoformat(),
            'end': tomorrow.isoformat(),
        }, method=method)
        status_code = getattr(raw_response, 'status_code', 200)
        if status_code != 405:
            raise FailedTest(
                message=f'Incorrect status code "{status_code}" when calling the API via method {method.__name__.upper()}. Expected status code: "405".',
                response=raw_response,
            )
    return TestResult()


# def test_error_for_non_timeslot_product(api_url, api_key, product_id, endpoint, version=2):
#     '''Testing timeslot availability for non timeslot product'''
#     tomorrow = get_tomorrow()
#     raw_response, response = client(f'{api_url}/v{version}/products/{product_id}/{endpoint}', api_key, {
#         'start': tomorrow.isoformat(),
#         'end': tomorrow.isoformat(),
#     })
#     api_error = get_api_error(raw_response, response)
#     expected_error = ApiError(
#         error_code=1002,
#         error='Timeslot product expected',
#         message=f'Requested timeslot availability for non timeslot product ID {product_id}',
#     )
#     return check_api_error(raw_response, api_error, expected_error)
