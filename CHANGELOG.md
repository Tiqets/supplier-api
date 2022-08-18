# Changelog

## 2.0.0

#### Product Catalog

- Endpoint with product catalog becomes required
- `use_timeslots` query parameter has been dropped
- New product fields:
  - `max_tickets_per_order` - each product can set a limit for a number of tickets in the order
  - `required_visitor_data` - each product can describe a list of additional data that are required from each visitor (full name, email, phone, address, passport id, date of birth)
  - `required_order_data` - data that is required to be delivered on the order level (not per visitor, eg. pickup location, nationality, zip code)
- Update the `/products` endpoint's response example to include examples of products with `required_visitor_data` and `required_order_data`.
- List the possible values for `required_order_data` and `required_visitor_data`.
- Update the endpoints' prefix from `v1/` to `v2/`.

#### Availability

- Timesloted and non-timesloted endpoints has been merged into a single endpoint `/v2/availability`
- Same response format for timesloted and non-timesloted products
- Each variant might return information about the current price
- `timeslot_id` query parameter has been dropped.
- Provide a better explanation of the meaning of the attribute `available_tickets`.
- Update the endpoints' prefix from `v1/` to `v2/`.

#### Reservation

- New error code `1003` that can be return if required visitor data wasn't delivered
- New fields:
  - `required_visitor_data`
  - `required_order_data`
- List the possible values for `required_order_data` and `required_visitor_data`.
- Update the `/reservation` endpoint's response examples to include examples with `required_order_data`.
- Update the endpoints' prefix from `v1/` to `v2/`.

#### Booking

- New optional header `TIQETS-TEST-ORDER`
- Rename attribute `barcode_position` in the endpoint's response to `barcode_scope`. Update the description of the attribute to make it easier to understand.
- Update the `/booking` endpoint's response examples to include examples of PDF barcodes and barcodes at `order` and `ticket` scope.
- Update the endpoints' prefix from `v1/` to `v2/`.

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
