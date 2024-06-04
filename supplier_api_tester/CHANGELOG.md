# Changelog

## 2.2.7

- Extended the maximum length of the variant ID from 16 chars to 64 chars and added another example to the list.
- Skip Reservation and Booking tests if the response from the API is unexpected.
- Upgrade `requests` library to version `2.32.0`

## 2.2.6

- Upgrade `clickclick` to v20.10.2

## 2.2.5

- Handle unexpected API responses when fetching availability. This will cause any test that requires corrected availability to be skipped.

## 2.2.3

- Add new test for testing the barcode formats.

## 2.2.2

- Additional warning if any customer data was requested
- Custom warning for incorrect values of required_order_data or required_visitor_data

## 2.2.1

- Booking test: recognizing a case in which the cancellation was accepted after the cancellation window
- Removing tests for not allowed methods

## 2.2.0

- Testing if the price in the reservation response is the same as it was in the availability response

## 2.1.0

- add new tests to validate the required additional visitor and order-level fields for the products in the catalog.
- upgrade `dacite` to v1.8.1

## 2.0.6

- bugfix: fix function `supplier_api_tester.v2.utils.adapters.get_api_error()` to handle non-Json error responses.

## 2.0.5

- update `requests` library to v2.31.0

## 2.0.4

- fix bug in reservation test when the time/date values of a timeslot contain a single digit. Eg. use `09:15` instead of `9:15`

## 2.0.3

- bump `requests` library to v2.28.2

## 2.0.2

- update the CLI testing tool to match the API specification v2.2.0

## 2.0.1

- Rename VariantPrice's field `face_value` to `amount`

## 2.0.0

- add support for API v2.0.0
- drop support for the CLI argument `--timeslots` (`-t`) in v2.0
- add new argument `--version-1` to the CLI tool to test an implementation against API v1.x or v2.x (default)

## 1.6.5

- Using time-based reference_id for booking

## 1.6.4

- security related update

## 1.6.3

- Add check if result can fit to terminal width

## 1.6.2

- Less calls for availability
- More sanity checks for availability
- Compatibility with python 3.7

## 1.6.1

- Add no cache headers

## 1.6.0

- Add new field `order_reference` to booking step.
- Start requiring it from 13th of January 2022

## 1.5.1

- Fix issue caused by unnecessary caching of the reservation test.

## 1.5.0

- Fix for showing response details
- New command: `supplier_products`
- Fixing typo in error message
- Using quotes when pointing to incorrect error messages
- Using cancellation endpoint only to check the error message if the product doesn't support cancellations
- New method for getting the catalog

## 1.4.10

- Adding tests for timeslots sanity check for timeslotted products

## 1.4.9

- Adding test for empty availability check for non timeslotted products

## 1.4.8

- Adding test for empty availability check

## 1.4.7

- Removing payload from the cancel booking call

## 1.4.6

- Fix for reporting connection errors

## 1.4.5

- Fix for cancelation test

## 1.4.4

- Fix for wrong variable name

## 1.4.3

- Updating availability tests

## 1.4.2

- Updating test-tool with testing cancellation

## 1.4.1

- Updating test-tool with testing validity of tickets for PDF type

## 1.4.0

- Displaying reports on failed tests

## 1.3.8

- Checking if the expiration date for reservation has any timezone instead of checking for UTC

## 1.3.7

- Adding option for running testing tool without colors on output (`--no-colors` or `-nc`)

## 1.3.6

- Updating the example of `BookingResponse`

## 1.3.5

- For for errors with receiving the 200 status code when 4xx is expected

## 1.3.4

- Fix for raising some exceptions in failed tests
- Replacing unused 2007 and 2008 errors with 2009

## 1.3.3

- Changing `use_timeslots` parameter from boolean to string.
