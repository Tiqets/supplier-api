PRODUCTS = [
    {
        'id': 'A300-FX',
        'name': 'A300-FX',
        'use_timeslots': True,
        'is_refundable': True,
        'cutoff_time': 24,
        'ticket_content_type': 'CODE128',
        'max_tickets_per_order': 10,
        'required_visitor_data': [],
        'required_order_data': [],
        # but this is not part of spec...
        'cancelled_bookings': [],
        'timeslot_available_tickets_as_sum': True  # available tickets is the sum among all variants
    },
    {
        'id': 'A400-FX',
        'name': 'A400-FX',
        'use_timeslots': True,
        'description': 'Test timeslot product',
        'is_refundable': False,
        'cutoff_time': 0,
        'ticket_content_type': 'CODE128',
        'max_tickets_per_order': 10,
        'required_visitor_data': ['FULL_NAME', 'PHONE'],
        'required_order_data': ['PICKUP_LOCATION', 'PASSPORT_ID'],
        'cancelled_bookings': [],
        'timeslot_available_tickets_as_sum': False
    },
    {
        'id': 'A500-FX',
        'name': 'A500-FX',
        'use_timeslots': False,
        'description': 'Test non timeslot product',
        'is_refundable': True,
        'cutoff_time': 0,
        'ticket_content_type': 'CODE128',
        'max_tickets_per_order': 25,
        'required_visitor_data': [],
        'required_order_data': ['PICKUP_LOCATION', 'PASSPORT_ID', 'FLIGHT_NUMBER'],
        'cancelled_bookings': [],
        'timeslot_available_tickets_as_sum': False
    },
    {
        'id': 'A550-FX',
        'name': 'A550-FX',
        'use_timeslots': False,
        'description': 'Test barcode',
        'is_refundable': True,
        'cutoff_time': 10,
        'ticket_content_type': 'PDF',
        'required_visitor_data': ['EMAIL', 'DATE_OF_BIRTH'],
        'required_order_data': [],
        'cancelled_bookings': [],
        'timeslot_available_tickets_as_sum': False
    },
    {
        'id': 'A600-FX',
        'name': 'A600-FX',
        'use_timeslots': False,
        'is_refundable': False,
        'cutoff_time': 0,
        'ticket_content_type': 'CODE128',
        'max_tickets_per_order': 5,
        'required_visitor_data': [],
        'required_order_data': ['NATIONALITY'],
        'cancelled_bookings': [],
        'timeslot_available_tickets_as_sum': False
    },
]
VARIANTS = ('Adult', 'Child')
MAX_DATE_RANGE = 6  # in months
PRODUCTS_CURRENCIES = {
    'A400-FX': 'USD',
}
