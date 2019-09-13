# Changelog

## 1.2.0

* Changing error name for the `2000` internal error code from "Incorrect date" to "Incorrect date format"
* Adding 4 new errors:
  * `2007` - Incorrect start date
  * `2008` - Date range is too wide
  * `2009` - Incorrect date
  * `3002` - Incorrect reservation ID
* Moving shared HTTP error status codes (`403`, `405`, `500`) to the beginning of the document.
* Incorrect type (`2004`) has been removed from availability endpoints

## 1.1.0

* Adding 1 new error:
  * `2006` - Superfluous timeslot parameter
* New `BookingResponse` property - `barcode_format`

