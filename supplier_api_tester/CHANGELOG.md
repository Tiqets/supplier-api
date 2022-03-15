# Changelog

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
