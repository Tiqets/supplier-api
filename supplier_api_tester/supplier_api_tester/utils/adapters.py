from datetime import date, datetime
from typing import List

import dacite

from ..exceptions import FailedTest
from ..models import ApiError, Booking, DailyAvailability, DailyVariants, Product, Reservation, Timeslot


def get_daily_availability(response) -> List[DailyAvailability]:
    '''Getting and testing response from the /dates endpoint'''
    if type(response) is not list:
        raise FailedTest('The response should be a JSON Array')
    try:
        days = [
            dacite.from_dict(
                data_class=DailyAvailability,
                data=day,
                config=dacite.Config(
                    type_hooks={date: date.fromisoformat},
                    strict=True,
                )
            )
            for day in response
        ]
    except (
        dacite.exceptions.WrongTypeError,
        dacite.exceptions.MissingValueError,
        dacite.exceptions.UnexpectedDataError,
    ):
        raise FailedTest('Incorrect JSON format in response from the /dates endpoint')
    return days


def get_variants(response) -> List[DailyVariants]:
    '''Getting and testing response from the /variants endpoint'''
    if type(response) is not list:
        raise FailedTest('The response should be a JSON Array')
    try:
        days = [
            dacite.from_dict(
                data_class=DailyVariants,
                data=day,
                config=dacite.Config(
                    type_hooks={date: date.fromisoformat},
                    strict=True,
                )
            )
            for day in response
        ]
    except (
        dacite.exceptions.WrongTypeError,
        dacite.exceptions.MissingValueError,
        dacite.exceptions.UnexpectedDataError,
    ):
        raise FailedTest('Incorrect JSON format in response from the /variants endpoint')
    return days


def get_timeslots(response) -> List[Timeslot]:
    '''Getting and testing response from the /timeslots endpoint'''
    if type(response) is not list:
        raise FailedTest('The response should be a JSON Array')
    try:
        days = [
            dacite.from_dict(
                data_class=Timeslot,
                data=day,
                config=dacite.Config(
                    type_hooks={date: date.fromisoformat},
                    strict=True,
                )
            )
            for day in response
        ]
    except (
        dacite.exceptions.WrongTypeError,
        dacite.exceptions.MissingValueError,
        dacite.exceptions.UnexpectedDataError,
    ):
        raise FailedTest('Incorrect JSON format in response from the /timeslots endpoint')
    return days


def get_products(response) -> List[Product]:
    '''Getting and testing response from the /products endpoint'''
    if type(response) is not list:
        raise FailedTest('The response should be a JSON Array')
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
    ):
        raise FailedTest('Incorrect JSON format in response from the /products endpoint')
    return products


def get_reservation(response) -> Reservation:
    '''Getting and testing response from the /reservation endpoint'''
    if type(response) is not dict:
        raise FailedTest('The response should be a JSON Object')
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
    ):
        raise FailedTest('Incorrect JSON format in response from the /reservation endpoint')


def get_booking(response) -> Booking:
    '''Getting and testing response from the /booking endpoint'''
    if type(response) is not dict:
        raise FailedTest('The response should be a JSON Object')
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
    ):
        raise FailedTest('Incorrect JSON format in response from the /booking endpoint')

    if booking.barcode_format not in ('QRCODE', 'CODE128', 'CODE39', 'ITF', 'DATAMATRIX', 'EAN13'):
        raise FailedTest(f'Incorrect barcode format ({booking.barcode_format})')
    if booking.barcode_position not in ('order', 'ticket'):
        raise FailedTest(f'Incorrect value in the barcode_position field ({booking.barcode_position})')
    if booking.barcode_position == 'order' and not booking.barcode:
        raise FailedTest('Barcode for the whole order is empty')
    if booking.barcode_position == 'ticket' and not booking.tickets:
        raise FailedTest('Tickets Array is empty')
    return booking


def get_api_error(response) -> ApiError:
    '''Unpacking 400 error JSON structure'''
    if type(response) is not dict:
        raise FailedTest('400 error response should be a JSON Object')
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
    ):
        raise FailedTest(f'Incorrect response format for 400 error')
