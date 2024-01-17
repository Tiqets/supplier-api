# Changelog

## 2.0.5

- Update catalog product `A600-FX` to use `AZTEC-BYTES` barcode format.

## 2.0.4

- upgrade version of `uWSGI` to `2.0.22`
- upgrade version of `Flask` to `2.2.5`

## 2.0.3

- Fix a bug in the Mock Server when handling reservation requests. For products that provide pricing
(`provides_pricing=True`) we need to return unit prices (`unit_price`) only for the variant ids that are part of the 
reservation.

## 2.0.2

- update the server to match the API specification v2.2.0

## 2.0.1

- Rename `face_value` to `amount` in availability data generator

## 2.0.0

- add support for the Supplier API v2.0
- remove support for the Supplier API v1.x

## 1.5.2

- bump `arrow` to version `0.15.1`

## 1.5.1

- Fix for checking the `order_reference`

## 1.5.0

- Add new field `order_reference`.
- Start requiring it from 13th of January 2022 otherwise raise error

## 1.4.4

- Fixing typo in error message
- Using quotes when pointing to incorrect arguments
- Fix for returning products without filtering by timeslots

## 1.4.3

- Removing redundant "/dates" endpoint

## 1.4.2

- Added cancellation endpoint

## 1.4.1

- Updating mock server with support for PDF type

## 1.3.4

- Replacing unused 2007 and 2008 errors with 2009

## 1.3.3

- Changing `use_timeslots` parameter from boolean to string.
