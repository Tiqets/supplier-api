from datetime import date, datetime, timedelta
import werkzeug

import arrow
from flask import Flask, request, jsonify

from .auth import authorization_header
from .validation import date_range_validator
from . import constants, error_handlers, exceptions, utils

app = Flask('supplier_server')
app.register_error_handler(werkzeug.exceptions.MethodNotAllowed, error_handlers.bad_method)
app.register_error_handler(werkzeug.exceptions.InternalServerError, error_handlers.server_error)
app.register_error_handler(exceptions.BadRequest, error_handlers.bad_request)


@app.route('/v1/products/<product_id>/dates')
@authorization_header
@date_range_validator
def available_dates(product_id: str):
    utils.check_product_id(product_id)
    start = utils.get_date(request.args, 'start')
    end = utils.get_date(request.args, 'end')
    if start > end:
        raise exceptions.BadRequest(2001, 'Incorrect date range', 'The end date cannot be earlier then start date')

    today = date.today()
    if end < today:
        return jsonify([])
    start = max(today, start)
    result = []
    day = start
    while day <= end:
        result.append({
            'date': day.isoformat(),
            'max_tickets': utils.get_availability(product_id, day)['max_tickets']
        })
        day = day + timedelta(days=1)
    return jsonify(result)


@app.route('/v1/products/<product_id>/variants')
@authorization_header
@date_range_validator
def availability_no_timeslots(product_id: str):
    utils.check_product_id(product_id)
    start = utils.get_date(request.args, 'start')
    end = utils.get_date(request.args, 'end')
    if start > end:
        raise exceptions.BadRequest(2001, 'Incorrect date range', 'The end date cannot be earlier then start date')
    today = date.today()
    if end < today:
        return jsonify([])
    start = max(today, start)
    result = []
    day = start
    while day <= end:
        result.append(utils.get_availability(product_id, day))
        day = day + timedelta(days=1)
    return jsonify(result)


@app.route('/v1/products/<product_id>/timeslots')
@authorization_header
@date_range_validator
def availability_timeslots(product_id: str):
    utils.check_product_id(product_id)
    start = utils.get_date(request.args, 'start')
    end = utils.get_date(request.args, 'end')
    if start > end:
        raise exceptions.BadRequest(2001, 'Incorrect date range', 'The end date cannot be earlier then start date')
    today = date.today()
    if end < today:
        return jsonify([])
    start = max(today, start)
    results = []
    day = start
    while day <= end:
        for timeslot in ('17:30', '19:30'):
            result = utils.get_availability(product_id, day)
            result['start'] = timeslot
            result['end'] = arrow.get(f'2000-01-01 {timeslot}').shift(hours=1).strftime('%H:%M')
            results.append(result)
        day = day + timedelta(days=1)
    return jsonify(results)


@app.route('/v1/products/<product_id>/reservation', methods=['POST'])
@authorization_header
def reservation(product_id: str):
    utils.check_product_id(product_id)
    day = utils.get_date(request.json, 'date')
    today_utc = datetime.utcnow().date()
    if day < today_utc:
        raise exceptions.BadRequest(2009, 'Incorrect date', 'Cannot use the past date')
    if day > arrow.get(today_utc).shift(months=constants.MAX_DATE_RANGE).date():
        raise exceptions.BadRequest(
            2009,
            'Incorrect date',
            f'This date is too far ahead in the future. You can book max {constants.MAX_DATE_RANGE} months ahead.'
        )
    timeslot = request.json.get('timeslot')
    tickets = request.json.get('tickets')
    if not tickets:
        raise exceptions.BadRequest(1000, 'Missing argument', 'Required argument tickets was not found')
    customer = request.json.get('customer')
    if not customer:
        raise exceptions.BadRequest(1000, 'Missing argument', 'Required argument customer was not found')
    availability = utils.get_availability(product_id, day)
    variant_quantity_map = {variant['id']: variant['max_tickets'] for variant in availability['variants']}
    for ticket in tickets:
        if ticket['quantity'] > variant_quantity_map[ticket['variant_id']]:
            raise exceptions.BadRequest(
                3000,
                'Availability error',
                f'Quantity ({ticket["quantity"]}) is not available anymore'
                f' for a given variant (id: {ticket["variant_id"]})'
            )
    expires_at = arrow.utcnow().shift(minutes=30)
    return {
        'reservation_id': utils.encode_reservation_id(expires_at, tickets),
        'expires_at': expires_at.isoformat(),
    }


@app.route('/v1/booking', methods=['POST'])
@authorization_header
def booking():
    reservation_id = request.json.get('reservation_id')
    if not reservation_id:
        raise exceptions.BadRequest(1000, 'Missing argument', 'Required argument \'reservation_id\' was not found')
    try:
        expires_at, variant_quantity_map = utils.decode_reservation_data(reservation_id)
    except:
        raise exceptions.BadRequest(3002, 'Incorrect reservation ID', 'Given reservation ID is incorrect')
    now = arrow.utcnow().datetime
    if now > expires_at:
        minutes_ago = round((now - expires_at).seconds / 60)
        raise exceptions.BadRequest(3001, 'Reservation expired', f'Your reservation has expired {minutes_ago} minutes ago')
    tickets = {}
    for variant_id, quantity in variant_quantity_map.items():
        barcodes = [str(utils.str_to_int(f'{reservation_id}{variant_id}{i}', 10)) for i in range(quantity)]
        tickets[variant_id] = barcodes
    return {
        'booking_id': f'{utils.str_to_int(expires_at.isoformat(), 10)}',
        'barcode_format': 'CODE128',
        'barcode_position': 'ticket',
        'tickets': tickets,
    }


def run():
    app.run(host='0.0.0.0', port=8000, debug=False)


if __name__ == '__main__':
    run()
