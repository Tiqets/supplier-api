# If multiple checks can be done using the same response
# then they should be done under a single test case.

from datetime import datetime, timedelta

from supplier_api_tester.v2.decorators import test_wrapper
from supplier_api_tester.v2.exceptions import FailedTest
from supplier_api_tester.v2.models import TestResult
from ..utils import availability


@test_wrapper
def test_next_30_days(api_url, api_key, product_id, version=2):
    """Checking availability for the next 30 days"""
    start_date = datetime.utcnow().date()
    end_date = start_date + timedelta(days=30)
    days, raw_response = availability.get_availability(
        api_url,
        api_key,
        product_id,
        version,
        start_date,
        end_date,
    )

    # non-zero availability check
    max_tickets_sum = sum(day.available_tickets for day in days)
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
    for day in days:
        days_counter += 1
        for variant in day.variants:
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

    return TestResult()


@test_wrapper
def test_missing_api_key(api_url, api_key, product_id, version=2):
    """Request without API-Key"""
    return availability.test_missing_api_key(api_url, api_key, product_id, 'availability', version=version)


@test_wrapper
def test_incorrect_api_key(api_url, api_key, product_id, version=2):
    """Request with incorrect API-Key"""
    return availability.test_incorrect_api_key(api_url, api_key, product_id, 'availability', version=version)


@test_wrapper
def test_missing_argument_error(api_url, api_key, product_id, version=2):
    """Testing missing argument errors"""
    return availability.test_missing_argument_error(api_url, api_key, product_id, 'availability', version=version)


@test_wrapper
def test_error_for_non_existing_product(api_url, api_key, product_id, version=2):
    """Testing availability for non existing product"""
    return availability.test_error_for_non_existing_product(
        api_url, api_key, product_id, 'availability', version=version
    )


@test_wrapper
def incorrect_date_format(api_url, api_key, product_id, version=2):
    """Checking incorrect date format"""
    return availability.incorrect_date_format(api_url, api_key, product_id, 'availability', version=version)


@test_wrapper
def end_before_start_error(api_url, api_key, product_id, version=2):
    """Checking incorrect range error"""
    return availability.end_before_start_error(api_url, api_key, product_id, 'availability', version=version)


@test_wrapper
def past_start_date(api_url, api_key, product_id, version=2):
    """Checking past date"""
    return availability.past_start_date(api_url, api_key, product_id, 'availability', version=version)


@test_wrapper
def huge_date_range(api_url, api_key, product_id, version=2):
    """Checking huge date range"""
    return availability.huge_date_range(api_url, api_key, product_id, 'availability', version=version)


@test_wrapper
def product_provides_pricing(api_url, api_key, product_id, version=2):
    """Testing optional price attribute in availability"""
    return availability.product_with_provides_pricing(api_url, api_key, product_id, 'availability', version=version)
