PRODUCTS = [
    {
        'id': 'A300-FX',
        'name': 'A300-FX',
        'use_timeslots': True,
        'is_refundable': True,
        'cutoff_time': 24,
    },
    {
        'id': 'A400-FX',
        'name': 'A400-FX',
        'use_timeslots': True,
        'is_refundable': True,
        'description': 'Test timeslot product',
        'is_refundable': False,
        'cutoff_time': 0,
    },
    {
        'id': 'A500-FX',
        'name': 'A500-FX',
        'use_timeslots': False,
        'description': 'Test non timeslot product',
        'is_refundable': True,
        'cutoff_time': 0,
    },
    {
        'id': 'A600-FX',
        'name': 'A600-FX',
        'use_timeslots': False,
        'is_refundable': False,
        'cutoff_time': 0,
    },
]
VARIANTS = ('Adult', 'Child')
MAX_DATE_RANGE = 6  # in months
