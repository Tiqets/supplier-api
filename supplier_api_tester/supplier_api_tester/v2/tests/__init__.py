from . import availability_variants
from . import booking
from . import product_catalog
from . import reservation

AVAILABILITY_TEST = (
    availability_variants.test_next_30_days,
    availability_variants.test_missing_api_key,
    availability_variants.test_incorrect_api_key,
    availability_variants.test_missing_argument_error,
    availability_variants.test_error_for_non_existing_product,
    availability_variants.incorrect_date_format,
    availability_variants.end_before_start_error,
    availability_variants.past_start_date,
    availability_variants.huge_date_range,
    availability_variants.not_allowed_method,
)

RESERVATION_TEST = (
    reservation.test_missing_api_key,
    reservation.test_incorrect_api_key,
    reservation.test_missing_argument_error,
    reservation.test_reservation,
    reservation.test_error_for_non_existing_product,
    reservation.test_incorrect_date_format,
    reservation.test_past_date,
    reservation.test_not_allowed_method,
)

BOOKING_TEST = (
    booking.test_missing_reservation_id,
    booking.test_missing_api_key,
    booking.test_incorrect_api_key,
    booking.test_not_allowed_method,
    booking.test_booking_incorrect_reservation_id,
    booking.test_booking,
    booking.test_cancellation,
)

PRODUCT_CATALOG = (
    product_catalog.test_get_products,
)