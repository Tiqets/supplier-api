from datetime import datetime, timedelta
from typing import Union

from supplier_api_tester import cache
from supplier_api_tester.client import client
from supplier_api_tester.exceptions import FailedTest
from supplier_api_tester.models import DailyAvailability, Timeslot
from supplier_api_tester.utils.adapters import get_variants, get_timeslots


def get_reservation_slot(api_url, api_key, product_id, timeslots: bool, version=1):
    '''Getting day of timeslot with at least one variant available.'''
    if cache.reservation_slot_cache:
        return cache.reservation_slot_cache
    start = datetime.utcnow().date()
    end = start + timedelta(days=30)
    if timeslots:
        response = client(f'{api_url}/v{version}/products/{product_id}/timeslots', api_key, {
            'start': start.isoformat(),
            'end': end.isoformat(),
        })
        days = get_timeslots(response)
    else:
        response = client(f'{api_url}/v{version}/products/{product_id}/variants', api_key, {
            'start': start.isoformat(),
            'end': end.isoformat(),
        })
        days = get_variants(response)

    days = [day for day in days if day.variants and day.max_tickets > 0]
    single_variant_item = None
    for day in days:
        variants_max_tickets = [v.max_tickets for v in day.variants if v.max_tickets > 0]
        if len(variants_max_tickets) > 1:
            # got multi variant slot
            cache.reservation_slot_cache = day
            return day
        if not single_variant_item:
            single_variant_item = day

    if not single_variant_item:
        raise FailedTest('There is no availability in the next 30 days to test a reservation.')
    cache.reservation_slot_cache = single_variant_item
    return single_variant_item


def get_payload_from_slot(slot: Union[DailyAvailability, Timeslot], variant_quantity=1, min_quantity=1):
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
