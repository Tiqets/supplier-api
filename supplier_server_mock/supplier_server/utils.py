from base64 import b64encode, b64decode
from datetime import date, datetime
import json
from decimal import Decimal
from typing import Dict, Optional
from typing import Set

from .constants import PRODUCTS, VARIANTS, PRODUCTS_CURRENCIES
from .exceptions import BadRequest


def get_date(data, name, required=True) -> Optional[date]:
    data_str = data.get(name)
    if not data_str:
        if not required:
            return None
        raise BadRequest(1000, 'Missing argument', f'Required argument "{name}" was not found')
    try:
        return date.fromisoformat(data_str)
    except ValueError:
        raise BadRequest(2000, 'Malformed datetime', f'Incorrect date format {data_str}, please use the YYYY-MM-DD format')


def check_product_id(product_id: str):
    if product_id not in [p['id'] for p in PRODUCTS]:
        raise BadRequest(1001, 'Missing product', f"Product with ID {product_id} doesn't exist")


def product_supports_timeslot(product_id: str) -> bool:
    return product_id in [p['id'] for p in PRODUCTS if p['use_timeslots']]


def product_provides_pricing(product_id: str) -> bool:
    return product_id in [p['id'] for p in PRODUCTS if p['provides_pricing']]


def product_required_additional_order_data(product_id: str) -> Set[str]:
    for p in PRODUCTS:
        if p['id'] == product_id:
            return set(p.get('required_order_data', []))
    return set()


def product_required_additional_visitors_data(product_id: str) -> Set[str]:
    for p in PRODUCTS:
        if p['id'] == product_id:
            return set(p.get('required_visitor_data', []))
    return set()


def timeslot_available_tickets_is_sum(product_id: str) -> bool:
    for p in PRODUCTS:
        if p['id'] == product_id:
            return p.get('_timeslot_available_tickets_as_sum')
    return False


def str_to_int(some_str, number_of_digits) -> int:
    return int(str(abs(hash(some_str)) % (10 ** 8))[:number_of_digits])


def get_availability(product_id: str, day: date) -> Dict:
    """
    Fake randomness generator.

    This supports both products with and without timeslots.

    :param product_id: the id of the product.
    :param day: get random availability for this day.
    :return availability data for a product and day with the following schema:
        {
            "YYYY-MM-DDTHH:MM": {
                "available_tickets": 100,
                "variants": [
                    {
                        "id": "",
                        "name": "",
                        "available_tickets": Int,
                        "price": {
                            "currency": "",
                            "amount": ""
                        }
                    },
                    {
                        "id": "",
                        "name": "",
                        "available_tickets": Int,
                        "price": {
                            "currency": "",
                            "amount": ""
                        }
                    }
                ]
            }
        }

        The `price` attribute is optional but MUST be present if the product's `provides_pricing` is `True`.
    """

    timeslots = [f'{day.isoformat()}T00:00']
    if product_supports_timeslot(product_id):
        timeslots = [f'{day.isoformat()}T17:30', f'{day.isoformat()}T19:30']

    result = {}

    if day.isoweekday() == 7:
        for timeslot in timeslots:
            result[timeslot] = {}
        return result

    number_of_digits = 1 if day.isoweekday() % 3 == 0 else 2

    product_supports_pricing = product_provides_pricing(product_id)

    for timeslot in timeslots:
        max_tickets = str_to_int(day.isoformat(), number_of_digits)
        tickets_left = max_tickets
        timeslot_available_tickets = 0

        variants = []
        for i, variant in enumerate(VARIANTS, 1):
            if i == len(VARIANTS):
                variant_max_ticket = tickets_left
            else:
                variant_max_ticket = min(
                    tickets_left,
                    str_to_int(f'{i * day.isoweekday()}{day.isoformat()}', number_of_digits)
                )
                tickets_left -= variant_max_ticket

            current_variant = {
                'id': str(i), 'name': variant, 'available_tickets': variant_max_ticket,
            }

            if product_supports_pricing:
                current_variant['price'] = {
                    'amount': f"{Decimal('12.45') * i}",
                    'currency': PRODUCTS_CURRENCIES.get(product_id, 'EUR'),
                }

            variants.append(current_variant)

            if variant_max_ticket > timeslot_available_tickets:
                timeslot_available_tickets = variant_max_ticket

        result[timeslot] = {
            'available_tickets': max_tickets if timeslot_available_tickets_is_sum else timeslot_available_tickets,
            'variants': variants,
        }

    return result


def encode_barcode(some_str):
    return b64encode(some_str.encode()).decode()


def encode_reservation_id(expires_at: datetime, tickets: list, product_id: str, booking_date: datetime) -> str:
    variants_quantity_map = {ticket['variant_id']: ticket['quantity'] for ticket in tickets}
    json_content = json.dumps([expires_at.isoformat(), variants_quantity_map, product_id, booking_date.isoformat()])
    return b64encode(json_content.encode()).replace(b'=', b'!').decode()


def encode_booking_id(booking_date_str, product_id):
    json_content = json.dumps([booking_date_str, product_id])
    return b64encode(json_content.encode()).replace(b'=', b'!').decode()


def decode_booking_data(booking_id: str):
    json_content = json.loads(b64decode(booking_id.replace('!', '=')).decode())
    return json_content[0], json_content[1]


def decode_reservation_data(reservation_id: str) -> tuple:
    json_content = json.loads(b64decode(reservation_id.replace('!', '=')).decode())
    expires_at = datetime.fromisoformat(json_content[0])
    variants_quantity_map = json_content[1]
    product_id = json_content[2]
    product_date = datetime.fromisoformat(json_content[3])
    return expires_at, variants_quantity_map, product_id, product_date
