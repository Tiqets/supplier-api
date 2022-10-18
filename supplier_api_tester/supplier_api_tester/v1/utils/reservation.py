from datetime import datetime, timedelta
from typing import Union

from supplier_api_tester.v1.exceptions import FailedTest
from supplier_api_tester.v1.models import DailyVariants, Timeslot
from supplier_api_tester.v1.utils.availability import (
    get_availability_timeslots,
    get_availability_variants,
)


def get_reservation_slot(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Getting day of timeslot with at least one variant available.'''
    start = datetime.utcnow().date()
    end = start + timedelta(days=30)
    if timeslots:
        days, raw_response = get_availability_timeslots(api_url, api_key, product_id, version, start, end)
    else:
        days, raw_response = get_availability_variants(api_url, api_key, product_id, version, start, end)

    days = [day for day in days if day.variants and day.max_tickets > 0]
    single_variant_item = None
    for day in days:
        variants_max_tickets = [v.max_tickets for v in day.variants if v.max_tickets > 0]
        if len(variants_max_tickets) > 1:
            # got multi variant slot
            return day
        if not single_variant_item:
            single_variant_item = day

    if not single_variant_item:
        raise FailedTest(
            message='There is no availability in the next 30 days to test a reservation.',
            response=raw_response,
        )
    return single_variant_item


def get_payload_from_slot(slot: Union[DailyVariants, Timeslot], variant_quantity=1, min_quantity=1):
    return {
        'date': slot.date.isoformat(),
        'tickets': [{
            'variant_id': variant.id,
            'quantity': variant_quantity,
        } for variant in slot.variants if variant.max_tickets >= min_quantity],
        'customer': {
            'first_name': 'Jon',
            'last_name': 'Snow',
            'email': 'tests@tiqets.com',
            'phone': '+31 85 888 4442',
            'country': 'NL',
        }
    }
