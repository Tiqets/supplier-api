# Changelog

## 2.2.0
#### Reservation
- Update the endpoint's response to accept an optional `unit_price` attribute that MUST be provided when the client makes a 
reservation for a product whose attribute `provides_pricing=true`. 

## 2.1.1
#### Booking Cancellation
- Deprecate status code `3004` `Tickets already used` and replace it with `3005` `Tickets already used`. 

## 2.1.0
#### Product Catalog
- New product fields:
  - `provides_pricing` - each product can enable or disable pricing by setting this field to `true` or `false`.
#### Reservation
- New variant field
  - `price` - each variant must provide this field when product is expected to have pricing with `provides_pricing=true` from Product Catalog.
- `required_order_data` and `required_visitor_data` now have lower case fields instead of upper case.
#### Booking Cancellation
- Add a status code `3004` `Tickets already used`

## 2.0.1

- In the (optional) `price` object of the `Variant` object in the `/v2/availability` endpoint's response,
  rename the `face_value` field `amount`

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

- Remove the endpoints `/products/{product-id}/timeslots` and `/products/{product-id}/variants` and replace them with a new endpoint `/v2/availability`.
- Change the schema of the endpoint's response.
- Same response format for products that support timeslots and products that do not.
- `timeslot_id` query parameter has been dropped.
- Provide a better explanation of the meaning of the attribute `available_tickets`.
- Update the endpoints' prefix from `v1/` to `v2/`.
- Deprecate the use of error code `2009`.
- Update description of error codes `2000`.
- Add new examples to show how to treat dates in the past while making requests to the availability endpoint.
- Remove attribute `id` for every timeslot from the availability endpoint's response schema.
- Update description of `/availability` endpoint.
- Each variant might return information about the current price via the optional attribute `price`.
- Add a new (optional) attribute `price` to every `Variant` object in the `/v2/availability` endpoint's response. The `Price`
  object has the following fields:
  - `face_value`: `string`
  - `currency`: `string`

  See the endpoint's documentation for examples.

#### Reservation

- New error code `1003` that can be return if required visitor data wasn't delivered
- New fields:
  - `required_visitor_data`
  - `required_order_data`
- List the possible values for `required_order_data` and `required_visitor_data`.
- Update the `/reservation` endpoint's response examples to include examples with `required_order_data`.
- Update the endpoints' prefix from `v1/` to `v2/`.
- Remove `timeslot_id` and `date` attributes.
- Add a new attribute `datetime` to the endpoint's payload to replace the attributes `timeslot_id` and `date`.
- Update the examples to include payloads with the new attribute `datetime`.
- Update description of error codes `2000`, `2002`, `2009` and `3000`.
- Remove error code `2006`.
- Remove error code `2010` in favor of error code `2005`.

#### Booking

- New optional header `TIQETS-TEST-ORDER`
- Rename attribute `barcode_position` in the endpoint's response to `barcode_scope`. Update the description of the attribute to make it easier to understand.
- Update the `/booking` endpoint's response examples to include examples of PDF barcodes and barcodes at `order` and `ticket` scope.
- Update the endpoints' prefix from `v1/` to `v2/`.

#### Concepts

- Add a section on Date and Times to explain the use of date/times across the API.

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
