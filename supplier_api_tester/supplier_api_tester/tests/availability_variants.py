from datetime import datetime, timedelta
from typing import List

import requests

from ..client import client
from ..decorators import test_wrapper
from ..exceptions import FailedTest
from ..models import TestResult, ApiError
from ..utils import availability
from ..utils.adapters import get_variants


@test_wrapper
def test_response_format(api_url, api_key, product_id, version=1):
    '''[Variants] Checking response format'''
    return availability.test_response_format(api_url, api_key, product_id, 'variants', get_variants, version=1)


@test_wrapper
def test_next_30_days(api_url, api_key, product_id, version=1):
    '''[Variants] Checking for any availability in the next 30 days'''
    return availability.test_next_30_days(api_url, api_key, product_id, 'variants', get_variants, version=1)


@test_wrapper
def test_missing_api_key(api_url, api_key, product_id, version=1):
    '''[Variants] Request without API-Key'''
    return availability.test_missing_api_key(api_url, api_key, product_id, 'variants', version=1)


@test_wrapper
def test_incorrect_api_key(api_url, api_key, product_id, version=1):
    '''[Variants] Request with incorrect API-Key'''
    return availability.test_incorrect_api_key(api_url, api_key, product_id, 'variants', version=1)


@test_wrapper
def test_missing_argument_error(api_url, api_key, product_id, version=1):
    '''[Variants] Testing missing argument errors'''
    return availability.test_missing_argument_error(api_url, api_key, product_id, 'variants', version=1)


@test_wrapper
def test_error_for_non_existing_product(api_url, api_key, product_id, version=1):
    '''[Variants] Testing availability for non existing product'''
    return availability.test_error_for_non_existing_product(api_url, api_key, product_id, 'variants', version=1)


@test_wrapper
def incorrect_date_format(api_url, api_key, product_id, version=1):
    '''[Variants] Checking incorrect date format'''
    return availability.incorrect_date_format(api_url, api_key, product_id, 'variants', version=1)


@test_wrapper
def end_before_start_error(api_url, api_key, product_id, version=1):
    '''[Variants] Checking incorrect range error'''
    return availability.end_before_start_error(api_url, api_key, product_id, 'variants', version=1)


@test_wrapper
def past_start_date(api_url, api_key, product_id, version=1):
    '''[Variants] Checking past date'''
    return availability.past_start_date(api_url, api_key, product_id, 'variants', version=1)


@test_wrapper
def huge_date_range(api_url, api_key, product_id, version=1):
    '''[Variants] Checking huge date range'''
    return availability.huge_date_range(api_url, api_key, product_id, 'variants', version=1)


@test_wrapper
def empty_availability(api_url, api_key, product_id, version=1):
    '''[Variants] Checking empty availability'''
    return availability.empty_availability(api_url, api_key, product_id, 'variants', version=1)


@test_wrapper
def not_allowed_method(api_url, api_key, product_id, version=1):
    '''[Variants] Testing methods that are not allowed'''
    return availability.not_allowed_method(api_url, api_key, product_id, 'variants', version=1)


@test_wrapper
def invalid_product(api_url, api_key, product_id, version=1):
    '''[Variants] Testing errors on timeslot product'''
    return availability.test_error_for_timeslot_product(api_url, api_key, product_id, 'variants', version=1)
