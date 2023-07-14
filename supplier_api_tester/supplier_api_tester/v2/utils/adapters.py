import base64
import binascii

from datetime import date, datetime
from typing import Dict
from typing import List

import dacite
from requests.models import Response

from supplier_api_tester.v2.exceptions import FailedTest
from supplier_api_tester.v2.models import ApiError, Booking, DailyVariants, Product, Reservation


def check_base64(item):
    try:
        return base64.b64encode(base64.b64decode(item)).decode() == item
    except binascii.Error:
        return False


def format_error_message(e: Exception) -> str:
    '''
    Method for enhancing the error messages from Dacite.
    '''
    if isinstance(e, dacite.exceptions.UnexpectedDataError):
        return str(e).replace(
            'to any data class field',
            'to any field from the specification'
        )
    return str(e)


def booking_pdf_validator(booking: Booking, raw_response: Response):
    if booking.barcode_scope == 'order':
        if not check_base64(booking.barcode):
            raise FailedTest(
                message="Error while decoding (base64) PDF voucher for the order",
                response=raw_response
        )
    elif booking.barcode_scope == 'ticket':
        for variant, barcodes in booking.tickets.items():
            for barcode in barcodes:
                if not check_base64(barcode):
                    raise FailedTest(
                        message="Error while decoding (base64) PDF voucher for the ticket",
                        response=raw_response
                    )


def parse_availability_variants(raw_response: Response, response: Dict) -> List[DailyVariants]:
    """Getting and testing response from the /availability endpoint"""
    if type(response) is not dict:
        raise FailedTest(
            message='The response should be a JSON Object',
            response=raw_response,
        )
    available_variants: List[DailyVariants] = []
    try:
        for day, day_availability in response.items():
            # extract timeslot component from the day value: YYYY-MM-DDTHH:MM
            date_time_value = datetime.fromisoformat(day)
            timeslot_hour: str = str(date_time_value.time().hour)
            timeslot_minutes: str = str(date_time_value.time().minute)
            available_variants.append(
                dacite.from_dict(
                    data_class=DailyVariants,
                    data={
                        'date': str(date_time_value.date()),
                        'timeslot': f'{timeslot_hour.zfill(2)}:{timeslot_minutes.zfill(2)}',
                        'available_tickets': day_availability.get('available_tickets', 0),
                        'variants': [
                            {**v}
                            for v in day_availability.get('variants', [])
                        ]
                    },
                    config=dacite.Config(
                        type_hooks={date: date.fromisoformat},
                        strict=True,
                    )
                )
            )
    except (
        dacite.exceptions.WrongTypeError,
        dacite.exceptions.MissingValueError,
        dacite.exceptions.UnexpectedDataError,
    ) as e:
        raise FailedTest(
            message=f'Incorrect JSON format in response from the /availability endpoint: {format_error_message(e)}',
            response=raw_response,
        )
    return available_variants


def get_products(raw_response: Response, response: Dict) -> List[Product]:
    """Getting and testing response from the /products endpoint"""
    if type(response) is not list:
        raise FailedTest(
            message='The response should be a JSON Array',
            response=raw_response,
        )
    try:
        products = [
            dacite.from_dict(
                data_class=Product,
                data=product,
            )
            for product in response
        ]
    except (
        dacite.exceptions.WrongTypeError,
        dacite.exceptions.MissingValueError,
        dacite.exceptions.UnexpectedDataError,
    ) as e:
        raise FailedTest(
            message=f'Incorrect JSON format in response from the /products endpoint: {format_error_message(e)}',
            response=raw_response,
        )
    return products


def get_reservation(raw_response: Response, response) -> Reservation:
    """Getting and testing response from the /reservation endpoint"""
    if type(response) is not dict:
        raise FailedTest(
            message='The response should be a JSON Object',
            response=raw_response,
        )
    try:
        return dacite.from_dict(
            data_class=Reservation,
            data=response,
            config=dacite.Config(
                type_hooks={datetime: datetime.fromisoformat},
                strict=True,
            )
        )
    except (
        dacite.exceptions.WrongTypeError,
        dacite.exceptions.MissingValueError,
        dacite.exceptions.UnexpectedDataError,
    ) as e:
        raise FailedTest(
            message=f'Incorrect JSON format in response from the /reservation endpoint: {format_error_message(e)}',
            response=raw_response,
        )


def get_booking(raw_response: Response, response) -> Booking:
    """Getting and testing response from the /booking endpoint"""
    if type(response) is not dict:
        raise FailedTest(
            message='The response should be a JSON Object',
            response=raw_response,
        )
    try:
        booking = dacite.from_dict(
            data_class=Booking,
            data=response,
            config=dacite.Config(strict=True)
        )
    except (
        dacite.exceptions.WrongTypeError,
        dacite.exceptions.MissingValueError,
        dacite.exceptions.UnexpectedDataError,
    ) as e:
        raise FailedTest(
            message=f'Incorrect JSON format in response from the /booking endpoint: {format_error_message(e)}',
            response=raw_response,
        )

    if booking.barcode_format not in ('QRCODE', 'CODE128', 'CODE39', 'ITF', 'DATAMATRIX', 'EAN13', 'PDF'):

        raise FailedTest(
            message=f'Incorrect barcode format ({booking.barcode_format})',
            response=raw_response,
        )

    if booking.barcode_format == 'PDF':
        booking_pdf_validator(booking, raw_response)

    if booking.barcode_scope not in ('order', 'ticket'):
        raise FailedTest(
            message=f'Incorrect value in the barcode_scope field: {booking.barcode_scope}',
            response=raw_response,
        )
    if booking.barcode_scope == 'order' and not booking.barcode:
        raise FailedTest(
            message='Barcode for the whole order is empty',
            response=raw_response,
        )
    if booking.barcode_scope == 'ticket' and not booking.tickets:
        raise FailedTest(
            message='Tickets Array is empty',
            response=raw_response,
        )
    return booking


def get_api_error(raw_response: Response, response) -> ApiError:
    """Unpacking 400 error JSON structure"""
    if raw_response.ok:
        raise FailedTest(
            message=f'Expected HTTP 400 but got HTTP {response.get("status_code")} instead.',
            response=raw_response,
        )
    if type(response) is not dict:
        raise FailedTest(
            message='400 error response should be a JSON Object',
            response=raw_response,
        )
    try:
        return dacite.from_dict(
            data_class=ApiError,
            data=response,
            config=dacite.Config(strict=True),
        )
    except (
        dacite.exceptions.WrongTypeError,
        dacite.exceptions.MissingValueError,
        dacite.exceptions.UnexpectedDataError,
    ) as e:
        raise FailedTest(
            message=f'Incorrect response format for 400 error: {format_error_message(e)}',
            response=raw_response,
        )
