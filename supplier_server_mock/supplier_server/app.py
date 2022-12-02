import binascii
from datetime import date, datetime, timedelta
from datetime import timezone
from typing import Dict
from typing import List

import werkzeug

import arrow
from flask import Flask, request, jsonify

from .utils import product_provides_pricing
from .auth import authorization_header
from .validation import date_range_validator
from . import constants, error_handlers, exceptions, utils

app = Flask('supplier_server')
app.register_error_handler(werkzeug.exceptions.MethodNotAllowed, error_handlers.bad_method)
app.register_error_handler(werkzeug.exceptions.InternalServerError, error_handlers.server_error)
app.register_error_handler(exceptions.BadRequest, error_handlers.bad_request)


@app.route('/v2/products')
@authorization_header
def products():
    # expose public attributes only
    return jsonify([{k: p[k] for k in p.keys() if not k.startswith('_')} for p in constants.PRODUCTS])


@app.route('/v2/products/<product_id>/availability')
@authorization_header
@date_range_validator
def availability(product_id: str):
    utils.check_product_id(product_id)
    start = utils.get_date(request.args, 'start')
    end = utils.get_date(request.args, 'end')
    if start > end:
        raise exceptions.BadRequest(2001, 'Incorrect date range', 'The end date cannot be earlier than start date')
    today = date.today()
    if end < today:
        return jsonify({})
    start = max(today, start)
    result = {}
    day = start
    while day <= end:
        result.update(utils.get_availability(product_id, day))
        day = day + timedelta(days=1)
    return jsonify(result)


@app.route('/v2/products/<product_id>/reservation', methods=['POST'])
@authorization_header
def reservation(product_id: str):
    utils.check_product_id(product_id)

    datetime_parameter_value = request.json.get('datetime')
    if not datetime_parameter_value:
        raise exceptions.BadRequest(1000, 'Missing argument', 'Required argument "datetime" was not found')

    tickets = request.json.get('tickets')
    if not tickets:
        raise exceptions.BadRequest(1000, 'Missing argument', 'Required argument "tickets" was not found')

    customer = request.json.get('customer')
    if not customer:
        raise exceptions.BadRequest(1000, 'Missing argument', 'Required argument "customer" was not found')

    # get the additional order-level information required by this product
    product_requires_additional_order_data = utils.product_required_additional_order_data(product_id)
    if product_requires_additional_order_data:
        required_order_data = request.json.get('required_order_data', {})
        required_order_data_keys = required_order_data.keys()
        missing_fields = product_requires_additional_order_data.difference(required_order_data_keys)
        if not required_order_data or missing_fields:
            raise exceptions.BadRequest(
                1003,
                'Missing required fields',
                f'Missing required additional order data: {",".join(missing_fields)}',
            )

    # extract date and timeslot information from datetime attribute
    try:
        datetime_parameter = datetime.strptime(datetime_parameter_value, '%Y-%m-%dT%H:%M')
        day = datetime_parameter.date()
        timeslot: str = datetime_parameter.time().strftime('%H:%M')
    except ValueError:
        raise exceptions.BadRequest(
            2000,
            'Malformed datetime',
            f'Expected datetime attribute with format YYYY-MM-DDTHH:MM'
        )

    today_utc = datetime.utcnow().date()
    if day < today_utc:
        raise exceptions.BadRequest(2009, 'Incorrect date', 'Cannot use the past date')

    if day > arrow.get(today_utc).shift(months=constants.MAX_DATE_RANGE).date():
        raise exceptions.BadRequest(
            2009,
            'Incorrect date',
            f'This date is too far ahead in the future. You can book max {constants.MAX_DATE_RANGE} months ahead.'
        )

    # if the product doesn't support timeslots then set the time component to 00:00 to extract availability for that
    # date/time
    timeslot_availability_key: str = (
        datetime_parameter_value if utils.product_supports_timeslot(product_id) else f'{day}T00:00'
    )

    product_availability: Dict = utils.get_availability(product_id, day)

    # map variant ids to available tickets
    variant_quantity_mapping: Dict[str, int] = {
        str(variant['id']): variant['available_tickets']
        for variant in product_availability.get(timeslot_availability_key, {}).get('variants', [])
    }

    # get the additional visitors-level information required by this product
    product_requires_additional_visitors_data = utils.product_required_additional_visitors_data(product_id)

    for ticket in tickets:
        ticket_variant_id = str(ticket['variant_id'])
        if (
                not variant_quantity_mapping.get(ticket_variant_id)
                or (ticket['quantity'] > variant_quantity_mapping.get(ticket_variant_id))
        ):
            raise exceptions.BadRequest(
                3000,
                'Availability error',
                f'The requested number of tickets is not longer available for the given variant and/or timeslot'
            )

        if product_requires_additional_visitors_data:
            required_visitor_data: List[Dict] = ticket.get('required_visitor_data', [])

            if not required_visitor_data or len(required_visitor_data) != ticket['quantity']:
                missing_qty = ticket['quantity'] - len(required_visitor_data)
                raise exceptions.BadRequest(
                    1003, 'Missing required fields', f'Missing visitor information for {missing_qty} visitors',
                )

            for visitor_data in required_visitor_data:
                missing_fields = product_requires_additional_visitors_data.difference(visitor_data.keys())
                if missing_fields:
                    raise exceptions.BadRequest(
                        1003,
                        'Missing required fields',
                        f'Missing required additional visitor data: {",".join(missing_fields)}'
                    )

    expires_at = arrow.utcnow().shift(minutes=30)
    reservation_date = datetime.fromisoformat(day.isoformat() + " " + timeslot)

    reservation_response = {
        'reservation_id': utils.encode_reservation_id(expires_at, tickets, product_id, reservation_date),
        'expires_at': expires_at.isoformat(),
    }

    if product_provides_pricing(product_id):
        variant_price_mapping: Dict[str, Dict] = {}  # map variant ids to price data
        for variant in product_availability.get(timeslot_availability_key, {}).get('variants', []):
            variant_price_mapping[variant['id']] = variant['price']

        reservation_response['unit_price'] = {}

        for variant_id in [str(ticket.get('variant_id')) for ticket in tickets]:
            if variant_id in variant_price_mapping:
                reservation_response['unit_price'][variant_id] = variant_price_mapping.get(variant_id, {})

    return jsonify(reservation_response)


@app.route('/v2/booking', methods=['POST'])
@authorization_header
def booking():
    reservation_id = request.json.get('reservation_id')
    order_reference = request.json.get('order_reference')

    if not reservation_id:
        raise exceptions.BadRequest(1000, 'Missing argument', 'Required argument "reservation_id" was not found')

    if not order_reference:
        raise exceptions.BadRequest(1000, 'Missing argument', 'Required argument "order_reference" was not found')

    try:
        expires_at, variant_quantity_map, product_id, booking_date = utils.decode_reservation_data(reservation_id)
    except Exception:
        raise exceptions.BadRequest(3002, 'Incorrect reservation ID', 'Given reservation ID is incorrect')

    now = arrow.utcnow().datetime
    if now > expires_at:
        minutes_ago = round((now - expires_at).seconds / 60)
        raise exceptions.BadRequest(
            3001, 'Reservation expired', f'Your reservation has expired {minutes_ago} minutes ago'
        )

    tickets = {}
    product = [p for p in constants.PRODUCTS if p["id"] == product_id][0]

    for variant_id, quantity in variant_quantity_map.items():
        if product["_ticket_content_type"] == "PDF":
            barcodes = [utils.encode_barcode(f'{reservation_id}{variant_id}{i}') for i in range(quantity)]
        else:
            barcodes = [str(utils.str_to_int(f'{reservation_id}{variant_id}{i}', 10)) for i in range(quantity)]
        tickets[variant_id] = barcodes

    booking_id = utils.encode_booking_id(booking_date.isoformat(), product_id)

    if booking_id in product['_cancelled_bookings']:
        del product['_cancelled_bookings'][booking_id]

    return jsonify(
        {
            'booking_id': booking_id,
            'barcode_format': product["_ticket_content_type"],
            'barcode_scope': 'ticket',
            'barcode': '',
            'tickets': tickets,
        }
    )


@app.route('/v2/booking/<booking_id>', methods=['DELETE'])
@authorization_header
def cancel_booking(booking_id):
    try:
        booked_for, product_id = utils.decode_booking_data(booking_id)
    except binascii.Error:
        raise exceptions.BadRequest(1004, 'Missing booking', f"Booking with ID {booking_id} doesn't exist")
    product = [p for p in constants.PRODUCTS if p["id"] == product_id][0]

    if not product["is_refundable"]:
        raise exceptions.BadRequest(
            3004,
            'Cancellation not possible',
            'The booking cannot be cancelled, the product does not allow cancellations',
        )

    if product['_tickets_already_used']:
        raise exceptions.BadRequest(
            3005,
            'Tickets already used',
            'The booking cannot be cancelled because tickets have already been used',
        )

    booking_for_time = datetime.fromisoformat(booked_for).replace(tzinfo=timezone.utc)
    cancellation_time = datetime.now(timezone.utc)
    if booking_for_time < cancellation_time:
        raise exceptions.BadRequest(2009, 'Incorrect date', 'Cannot use the past date')

    difference = booking_for_time - cancellation_time
    hours_in_advance = round(difference.total_seconds()/3600)
    if product["cutoff_time"] != 0 and product["cutoff_time"] > hours_in_advance:
        raise exceptions.BadRequest(
            2009, 'Incorrect date', f'The booking can only be cancelled {product["cutoff_time"]} hours in advance'
        )

    if booking_id in product["_cancelled_bookings"]:
        raise exceptions.BadRequest(
            3003, 'Already cancelled', f'The booking with ID {booking_id} was already cancelled'
        )

    # if we want to test double cancellation, we need to store the cancelled booking id somewhere
    product["_cancelled_bookings"][booking_id] = True
    return '', 204


def run():
    app.run(host='0.0.0.0', port=8000, debug=False)


if __name__ == '__main__':
    run()
