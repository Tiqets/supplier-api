# If multiple checks can be done using the same response
# then they should be done under a single test case.

from datetime import datetime, timedelta

from ..decorators import test_wrapper
from ..exceptions import FailedTest
from ..models import TestResult
from ..utils import availability


@test_wrapper
def test_next_30_days(api_url, api_key, product_id, version=1):
    '''[Timeslots] Checking availability for the next 30 days'''
    start_date = datetime.utcnow().date()
    end_date = start_date + timedelta(days=30)
    timeslots, raw_response = availability.get_availability_timeslots(
        api_url,
        api_key,
        product_id,
        version,
        start_date,
        end_date,
    )

    # non-zero availability check
    max_tickets_sum = sum(timeslot.max_tickets for timeslot in timeslots)
    if max_tickets_sum <= 0:
        raise FailedTest(
            message='There is no availability for next 30 days',
            response=raw_response,
        )

    # variant IDs uniqueness
    variant_ids = set()
    variant_name_id_map = {}
    variant_counter = 0
    days_counter = 0
    previous_day = None
    for timeslot in timeslots:
        if timeslot.date != previous_day:
            days_counter += 1
            previous_day = timeslot.date
        for variant in timeslot.variants:
            # checking if one variant name always have the same ID
            if variant.name in variant_name_id_map:
                if variant.id != variant_name_id_map[variant.name]:
                    raise FailedTest(
                        message=f'Variant {variant.name} should always have the same ID.',
                        response=raw_response,
                    )
            else:
                variant_name_id_map[variant.name] = variant.id

            variant_counter += 1
            variant_ids.add(variant.id)

        # checking number of unique variants in timespan of 7 days
        if days_counter == 7:
            days_counter = 0
            if len(variant_ids) > 20:
                return TestResult(
                    status=1,
                    message=(
                        'More then 20 unique variants were found in a timespan of 7 days. '
                        'Make sure that this is not an error. Variants should not be unique for '
                        'each day.'
                    ),
                )
            variant_ids = set()

    # Detecting single timeslot configuration
    dates = {t.date for t in timeslots}
    unique_dates = set(dates)
    if len(unique_dates) == len(dates):
        unique_starts_ends = {f'{t.start}-{t.end}' for t in timeslots}
        if len(unique_starts_ends) == 1:
            raise FailedTest(
            message='If a product contains only a single timeslot at the same time every day, then please implement it as a non-timesloted product',
            response=raw_response,
            )

    # Checking if timslots are uniqe for each day
    unique_dates_starts_ends = {f'{t.date}-{t.start}-{t.end}' for t in timeslots}
    if len(timeslots) != len(unique_dates_starts_ends):
        raise FailedTest(
            message='Timeslots cannot be duplicated',
            response=raw_response,
        )

    return TestResult()


@test_wrapper
def test_missing_api_key(api_url, api_key, product_id, version=1):
    '''[Timeslots] Request without API-Key'''
    return availability.test_missing_api_key(api_url, api_key, product_id, 'timeslots', version=1)


@test_wrapper
def test_incorrect_api_key(api_url, api_key, product_id, version=1):
    '''[Timeslots] Request with incorrect API-Key'''
    return availability.test_incorrect_api_key(api_url, api_key, product_id, 'timeslots', version=1)


@test_wrapper
def test_missing_argument_error(api_url, api_key, product_id, version=1):
    '''[Timeslots] Testing missing argument errors'''
    return availability.test_missing_argument_error(api_url, api_key, product_id, 'timeslots', version=1)


@test_wrapper
def test_error_for_non_existing_product(api_url, api_key, product_id, version=1):
    '''[Timeslots] Testing availability for non existing product'''
    return availability.test_error_for_non_existing_product(api_url, api_key, product_id, 'timeslots', version=1)


@test_wrapper
def incorrect_date_format(api_url, api_key, product_id, version=1):
    '''[Timeslots] Checking incorrect date format'''
    return availability.incorrect_date_format(api_url, api_key, product_id, 'timeslots', version=1)


@test_wrapper
def end_before_start_error(api_url, api_key, product_id, version=1):
    '''[Timeslots] Checking incorrect range error'''
    return availability.end_before_start_error(api_url, api_key, product_id, 'timeslots', version=1)


@test_wrapper
def past_start_date(api_url, api_key, product_id, version=1):
    '''[Timeslots] Checking past date'''
    return availability.past_start_date(api_url, api_key, product_id, 'timeslots', version=1)


@test_wrapper
def huge_date_range(api_url, api_key, product_id, version=1):
    '''[Timeslots] Checking huge date range'''
    return availability.huge_date_range(api_url, api_key, product_id, 'timeslots', version=1)


@test_wrapper
def empty_availability(api_url, api_key, product_id, version=1):
    '''[Timeslots] Checking empty availability'''
    return availability.empty_availability(api_url, api_key, product_id, 'timeslots', version=1)


@test_wrapper
def not_allowed_method(api_url, api_key, product_id, version=1):
    '''[Timeslots] Testing methods that are not allowed'''
    return availability.not_allowed_method(api_url, api_key, product_id, 'timeslots', version=1)


@test_wrapper
def invalid_product(api_url, api_key, product_id, version=1):
    '''[Timeslots] Testing errors on invalid (non-timeslot) product'''
    return availability.test_error_for_non_timeslot_product(api_url, api_key, product_id, 'timeslots', version=1)
