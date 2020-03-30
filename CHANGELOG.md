# Changelog

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
- Adding 4 new errors:
  - `2007` - Incorrect start date
  - `2008` - Date range is too wide
  - `2009` - Incorrect date
  - `3002` - Incorrect reservation ID
- Moving shared HTTP error status codes (`403`, `405`, `500`) to the beginning of the document.
- Incorrect type (`2004`) has been removed from availability endpoints

## 1.1.0

- Adding 1 new error:
  - `2006` - Superfluous timeslot parameter
- New `BookingResponse` property - `barcode_format`
