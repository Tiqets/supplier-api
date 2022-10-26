from datetime import datetime, timedelta
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from supplier_api_tester.v2.exceptions import FailedTest
from supplier_api_tester.v2.models import DailyVariants, Timeslot
from supplier_api_tester.v2.models import Product
from supplier_api_tester.v2.utils.availability import get_availability
from supplier_api_tester.v2.utils.catalog import get_catalog


def get_reservation_slot(api_url, api_key, product_id, version=2) -> Optional[DailyVariants]:
    """Getting day of timeslot with at least one variant available."""
    start = datetime.utcnow().date()
    end = start + timedelta(days=30)
    days, raw_response = get_availability(api_url, api_key, product_id, version, start, end)

    days: List[DailyVariants] = [day for day in days if day.variants and day.available_tickets > 0]
    single_variant_item = None
    for day in days:
        variants_max_tickets = [v.available_tickets for v in day.variants if v.available_tickets > 0]
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


def get_payload_for_reservation(
        api_url: str,
        api_key: str,
        product_id: str,
        slot: Union[DailyVariants, Timeslot],
        variant_quantity=1,
        min_quantity=2,
        with_additional_order_data: bool = True,
        with_additional_visitors_data: bool = True,
) -> Dict:
    # get product information to determine the required additional (order, visitors) data
    _, products = get_catalog(api_url, api_key, version=2)
    product = [product for product in products if product.id == product_id][0]
    payload = {
        'datetime': (
            f'{slot.date.isoformat()}T{slot.timeslot}'
            if product.use_timeslots
            else f'{slot.date.isoformat()}T00:00'
        ),
        'customer': {
            'first_name': 'Jon',
            'last_name': 'Snow',
            'email': 'tests@tiqets.com',
            'phone': '+31 85 888 4442',
            'country': 'NL',
        }
    }

    tickets = []

    for variant in slot.variants:
        if variant.available_tickets >= min_quantity:
            ticket = {
                'variant_id': variant.id,
                'quantity': variant_quantity,
            }

            if product.required_visitor_data and with_additional_visitors_data:
                ticket['required_visitor_data'] = get_required_visitors_data_payload(
                    product.required_visitor_data, variant_quantity
                )

            tickets.append(ticket)

    payload['tickets'] = tickets

    if with_additional_order_data:
        required_order_data: Dict = get_required_order_data_payload(product)
        if required_order_data:
            payload['required_order_data'] = required_order_data

    return payload


def get_required_order_data_payload(product: Product) -> Dict:
    if not product.required_order_data:
        return {}

    required_order_data: Dict = {}
    for required_field_name in product.required_order_data:
        # get a (random) value for the field
        required_order_data[required_field_name] = f'test {required_field_name.lower()}'
    return required_order_data


def get_required_visitors_data_payload(required_visitor_data: List[str], variant_quantity: int) -> List[Dict]:
    required_visitors_data: List[Dict] = []
    for i in range(1, variant_quantity + 1):
        data = {}
        for required_field_name in required_visitor_data:
            # get a (random) value for the field
            data[required_field_name] = f'test {required_field_name.lower()} {i}'
        required_visitors_data.append(data)
    return required_visitors_data
