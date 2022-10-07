PRODUCTS = [
    {
        'id': 'A300-FX',
        'name': 'A300-FX',
        'use_timeslots': True,
        'is_refundable': True,
        'cutoff_time': 24,
        'max_tickets_per_order': 10,
        'required_visitor_data': [],
        'required_order_data': [],
        # but these fields are not part of spec...
        '_ticket_content_type': 'CODE128',
        '_cancelled_bookings': [],
        '_timeslot_available_tickets_as_sum': True  # available tickets is the sum among all variants
    },
    {
        'id': 'A400-FX',
        'name': 'A400-FX',
        'use_timeslots': True,
        'description': 'Test timeslot product',
        'is_refundable': False,
        'cutoff_time': 0,
        'max_tickets_per_order': 10,
        'required_visitor_data': ['FULL_NAME', 'PHONE'],
        'required_order_data': ['PICKUP_LOCATION', 'PASSPORT_ID'],
        '_ticket_content_type': 'CODE128',
        '_cancelled_bookings': [],
        '_timeslot_available_tickets_as_sum': False
    },
    {
        'id': 'A500-FX',
        'name': 'A500-FX',
        'use_timeslots': False,
        'description': 'Test non timeslot product',
        'is_refundable': True,
        'cutoff_time': 0,
        'max_tickets_per_order': 25,
        'required_visitor_data': [],
        'required_order_data': ['PICKUP_LOCATION', 'PASSPORT_ID', 'FLIGHT_NUMBER'],
        '_ticket_content_type': 'CODE128',
        '_cancelled_bookings': [],
        '_timeslot_available_tickets_as_sum': False
    },
    {
        'id': 'A550-FX',
        'name': 'A550-FX',
        'use_timeslots': False,
        'description': 'Test barcode',
        'is_refundable': True,
        'cutoff_time': 10,
        'required_visitor_data': ['EMAIL', 'DATE_OF_BIRTH'],
        'required_order_data': [],
        '_ticket_content_type': 'PDF',
        '_cancelled_bookings': [],
        '_timeslot_available_tickets_as_sum': False
    },
    {
        'id': 'A600-FX',
        'name': 'A600-FX',
        'use_timeslots': False,
        'is_refundable': False,
        'cutoff_time': 0,
        'max_tickets_per_order': 5,
        'required_visitor_data': [],
        'required_order_data': ['NATIONALITY'],
        '_ticket_content_type': 'CODE128',
        '_cancelled_bookings': [],
        '_timeslot_available_tickets_as_sum': False
    },
]
VARIANTS = ('Adult', 'Child')
MAX_DATE_RANGE = 6  # in months
PRODUCTS_CURRENCIES = {
    'A400-FX': 'USD',
}
