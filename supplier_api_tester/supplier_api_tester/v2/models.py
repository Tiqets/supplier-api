from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Optional, List, Dict


class RequiredOrderData(Enum):
    pickup_location = 'pickup_location'
    dropoff_location = 'dropoff_location'
    nationality = 'nationality'
    flight_number = 'flight_number'
    passport_id = 'passport_id'


class RequiredVisitorData(Enum):
    full_name = 'full_name'
    email = 'email'
    phone = 'phone'
    address = 'address'
    passport_id = 'passport_id'
    date_of_birth = 'date_of_birth'


@dataclass
class Response:
    url: str
    status_code: int
    headers: Dict[str, str]
    payload: Optional[str] = None
    body: Optional[str] = None


@dataclass
class TestResult:
    title: str = ''
    status: int = 0
    message: Optional[str] = None
    duration: int = 0
    response: Optional[Response] = None

    @property
    def status_text(self):
        return {
            0: 'OK',
            1: 'WARNING',
            2: 'ERROR',
        }[self.status]

    @property
    def is_ok(self):
        return self.status == 0

    @property
    def is_warning(self):
        return self.status == 1

    @property
    def is_error(self):
        return self.status == 2


@dataclass
class Product:
    id: str
    name: str
    use_timeslots: bool
    description: Optional[str]
    is_refundable: bool
    cutoff_time: int
    provides_pricing: bool
    required_order_data: Optional[List[RequiredOrderData]] = None
    required_visitor_data: Optional[List[RequiredVisitorData]] = None


@dataclass
class VariantPrice:
    currency: str
    amount: str

    def __str__(self):
        return f'{self.amount} {self.currency}'


@dataclass
class Variant:
    id: str
    name: str
    available_tickets: int
    price: Optional[VariantPrice] = None


@dataclass
class DailyVariants:
    date: date
    timeslot: str
    available_tickets: int
    variants: List[Variant]


@dataclass
class Timeslot:
    date: date
    start: str
    end: str
    max_tickets: int
    variants: List[Variant]


@dataclass
class ApiError:
    error: str
    error_code: int
    message: str


@dataclass
class Reservation:
    reservation_id: str
    expires_at: datetime
    unit_price: Optional[Dict[str, VariantPrice]] = None


@dataclass
class Booking:
    booking_id: str
    barcode_format: str
    barcode_scope: str
    barcode: Optional[str]
    tickets: Optional[Dict[str, List[str]]]
