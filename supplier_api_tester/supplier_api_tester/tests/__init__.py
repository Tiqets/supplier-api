from . import availability_dates
from . import availability_variants
from . import availability_timeslots
from . import reservation
from . import booking

AVAILABILITY_TEST = (
    availability_dates.test_response_format,
    availability_dates.test_next_30_days,
    availability_dates.test_missing_api_key,
    availability_dates.test_incorrect_api_key,
    availability_dates.test_missing_argument_error,
    availability_dates.test_error_for_non_existing_product,
    availability_dates.incorrect_date_format,
    availability_dates.end_before_start_error,
    availability_dates.not_allowed_method,
)

AVAILABILITY_VARIANTS_TEST = (
    availability_variants.test_response_format,
    availability_variants.test_next_30_days,
    availability_variants.test_missing_api_key,
    availability_variants.test_incorrect_api_key,
    availability_variants.test_missing_argument_error,
    availability_variants.test_error_for_non_existing_product,
    availability_variants.incorrect_date_format,
    availability_variants.end_before_start_error,
    availability_variants.not_allowed_method,
)

AVAILABILITY_TIMESLOTS_TEST = (
    availability_timeslots.test_next_30_days,
    availability_timeslots.test_response_format,
    availability_timeslots.test_missing_api_key,
    availability_timeslots.test_incorrect_api_key,
    availability_timeslots.test_missing_argument_error,
    availability_timeslots.test_error_for_non_existing_product,
    availability_timeslots.incorrect_date_format,
    availability_timeslots.end_before_start_error,
    availability_timeslots.not_allowed_method,
)

RESERVATION_TEST = (
    reservation.test_missing_api_key,
    reservation.test_incorrect_api_key,
    reservation.test_missing_argument_error,
    reservation.test_reservation,
    reservation.test_error_for_non_existing_product,
    reservation.test_incorrect_date_format,
    reservation.test_not_allowed_method,
)

BOOKING_TEST = (
    booking.test_missing_reservation_id,
    booking.test_missing_api_key,
    booking.test_incorrect_api_key,
    booking.test_not_allowed_method,
    booking.test_booking,
)
