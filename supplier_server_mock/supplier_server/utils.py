from base64 import b64encode, b64decode
from datetime import date, datetime
import json

from .constants import PRODUCTS, VARIANTS
from .exceptions import BadRequest


def get_date(data, name, required=True):
    data_str = data.get(name)
    if not data_str:
        if not required:
            return None
        raise BadRequest(1000, 'Missing argument', f'Required argument "{name}" was not found')
    try:
        return date.fromisoformat(data_str)
    except ValueError:
        raise BadRequest(2000, 'Incorrect date format', f'Incorrect date format {data_str}, please use the YYYY-MM-DD format')


def check_product_id(product_id: str):
    if product_id not in [p['id'] for p in PRODUCTS]:
        raise BadRequest(1001, 'Missing product', f"Product with ID {product_id} doesn't exist")


def check_timeslot_product(product_id: str):
    if product_id not in [p['id'] for p in PRODUCTS if p['use_timeslots']]:
        raise BadRequest(
            1002, 'Timeslot product expected', f'Requested timeslot availability for non timeslot product ID {product_id}'
        )


def check_non_timeslot_product(product_id: str):
    if product_id not in [p['id'] for p in PRODUCTS if not p['use_timeslots']]:
        raise BadRequest(
            1003, 'Non-timeslot product expected', f'Requested non timeslot availability for timeslot product ID {product_id}'
        )


def str_to_int(some_str, number_of_digits) -> int:
    return int(str(abs(hash(some_str)) % (10 ** 8))[:number_of_digits])


def get_availability(product_id: str, day: date):
    '''
    Fake randomness generator.
    '''
    if day.isoweekday() == 7:
        return {
            'date': day.isoformat(),
            'max_tickets': 0,
            "variants": []
        }
    variants = []
    number_of_digits = 1 if day.isoweekday() % 3 == 0 else 2
    max_tickets = str_to_int(day.isoformat(), number_of_digits)
    tickets_left = max_tickets
    for i, variant in enumerate(VARIANTS, 1):
        if i == len(VARIANTS):
            variant_max_ticket = tickets_left
        else:
            variant_max_ticket = min(
                tickets_left,
                str_to_int(f'{i * day.isoweekday()}{day.isoformat()}', number_of_digits)
            )
            tickets_left -= variant_max_ticket
        variants.append({
            "id": str(i),
            "name": variant,
            "max_tickets": variant_max_ticket,
        })
    return {
        'date': day.isoformat(),
        'max_tickets': max_tickets,
        "variants": variants,
    }

def encode_barcode(some_str):
    return b64encode(some_str.encode()).decode()


def encode_reservation_id(expires_at: datetime, tickets: list, product_id: str, booking_date: datetime) -> str:
    variants_quantity_map = {ticket['variant_id']: ticket['quantity'] for ticket in tickets}
    json_content = json.dumps([expires_at.isoformat(), variants_quantity_map, product_id, booking_date.isoformat()])
    return b64encode(json_content.encode()).replace(b'=', b'!').decode()

def encode_booking_id(booking_date_str, product_id):
    json_content = json.dumps([booking_date_str,product_id])
    return b64encode(json_content.encode()).replace(b'=', b'!').decode()

def decode_booking_data(booking_id:str):
    json_content = json.loads(b64decode(booking_id.replace('!', '=')).decode())
    booking_date, product_id = json_content
    return booking_date, product_id

def decode_reservation_data(reservation_id: str) -> tuple:
    json_content = json.loads(b64decode(reservation_id.replace('!', '=')).decode())
    expires_at = datetime.fromisoformat(json_content[0])
    variants_quantity_map = json_content[1]
    product_id = json_content[2]
    date = datetime.fromisoformat(json_content[3])
    # variants_quantity_map, product_id, date = json_content[1:]
    return expires_at, variants_quantity_map, product_id, date
