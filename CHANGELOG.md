# Changelog

## 1.6.2
- Added a warning that this version is no longer supported for new integrators
- Added error code 3005 "tickets already used" error, just like in V2

## 1.6.0

- Add new field `order_reference` to booking step.
- Start requiring it from 13th of January 2022

## 1.4.2
- Removing "/dates" endpoint as redundant

## 1.4.1
- Adding "PDF" as supported "barcode_format"

## 1.4.0

- Adding endpoint for cancellations
- Adding two new product fields:
  - `is_refundable` - product supports cancellations
  - `cutoff_time` - the minimal number of hours before the booking date/time for the cancellation to be successful. 0 means no limit.

## 1.3.3

- Changing `use_timeslots` parameter from boolean to string.

## 1.3.2

- Fix date format display in API errors.

## 1.3.1

- Update `Product.use_timeslot` to `Product.use_timeslots` in supplier tester and mock server.
- Make `product-id` not required on product catalog tests.

## 1.3.0

- Adding product catalog endpoint
- Adding 2 new errors:
  - `1002` - Timeslot product expected
  - `1003` - Non-timeslot product expected

## 1.2.0

- Changing error name for the `2000` internal error code from "Incorrect date" to "Incorrect date format"
- Adding 2 new errors:
  - `2009` - Incorrect date
  - `3002` - Incorrect reservation ID
- Moving shared HTTP error status codes (`403`, `405`, `500`) to the beginning of the document.
- Incorrect type (`2004`) has been removed from availability endpoints

## 1.1.0

- Adding 1 new error:
  - `2006` - Superfluous timeslot parameter
- New `BookingResponse` property - `barcode_format`
