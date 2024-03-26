# Supplier API Testing Tool

![CLI tool screenshot](../docs/clitool.png)

## Requirements

Python 3.7+

## Installation

```sh
pip install supplier-api-tester
```

## Usage

The CLI Testing Tool supports both API v1.x and v2.x. By default, the CLI runs all the tests for API v2.x. 

If you wish to test your API implementation based on the v1 specification then you can pass the argument `--version` 
(or `-v`) in the CLI to enable v1 testing.

For more details on how to test your v1-complaint implementation please refer to the [API docs for V1](https://tiqets.github.io/supplier-api/v1.html). 

For example, the following command will test your API implementation according to the v1 specification:

```sh
supplier_products -u 'http://localhost:8000' -k 'secret' -v 1
```

Listing the products catalog:

```sh
supplier_products -u 'http://localhost:8000' -k 'secret' -v 2

A300-FX
ID: A300-FX
Timeslots: yes
Refundable: yes
Cutoff time: 24
Provides Pricing: yes

A400-FX
ID: A400-FX
Timeslots: yes
Refundable: no
Cutoff time: 0
Required Additional Order Data: pickup_location, passport_id
Required Additional Visitors Data: full_name, phone
Provides Pricing: no

A500-FX
ID: A500-FX
Timeslots: no
Refundable: yes
Cutoff time: 0
Required Additional Order Data: pickup_location, passport_id, flight_number
Provides Pricing: yes

A550-FX
ID: A550-FX
Timeslots: no
Refundable: yes
Cutoff time: 10
Required Additional Visitors Data: email, date_of_birth
Provides Pricing: no

A600-FX
ID: A600-FX
Timeslots: no
Refundable: no
Cutoff time: 0
Required Additional Order Data: nationality
Provides Pricing: no

Products found: 5
```

Testing tool usage:
```
supplier_tester --help
Usage: supplier_tester [OPTIONS]

  Test your Supplier API implementation

Options:
  -u, --url TEXT         [required]
  -k, --api-key TEXT     [required]
  -p, --product-id TEXT  Product ID to call tests on. Required with -a and -t flags
  -t, --timeslots        Use timeslots
  -a, --availability     Run availability tests
  -r, --reservation      Run reservation tests
  -b, --booking          Run booking tests
  -c, --catalog          Run product catalog tests
  -nc, --no-colors       Not using colors on output
  -v, --version          Choosing the API version
  --help                 Show this message and exit
```

Running all tests:

```sh
supplier_tester -u 'http://localhost:8000' -k 'secret' -p 'A500-FX' -v 2
```

Running only availability tests:

```sh
supplier_tester -u 'http://localhost:8000' -k 'secret' -p 'A500-FX' -a -v 2
```

Test example:

```sh
supplier_tester -u 'http://localhost:8000' -k 'secret' -p 'A500-FX' -v 2

──────────────────
AVAILABILITY TESTS
──────────────────

█  # 1 [ 12ms] Checking availability for the next 30 days
█  # 2 [  4ms] Request without API-Key
█  # 3 [  3ms] Request with incorrect API-Key
█  # 4 [  9ms] Testing missing argument errors
█  # 5 [  3ms] Testing availability for non existing product
█  # 6 [  7ms] Checking incorrect date format
█  # 7 [  3ms] Checking incorrect range error
█  # 8 [  3ms] Checking past date
█  # 9 [128ms] Checking huge date range
█  #10 [ 10ms] Testing optional price attribute in availability

─────────────────
RESERVATION TESTS
─────────────────

█  # 1 [  5ms] Request without API-Key
█  # 2 [  4ms] Request with incorrect API-Key
█  # 3 [ 20ms] Testing missing argument errors
█  # 4 [ 17ms] Reserving tickets for at least 1 variant
█  # 5 [ 13ms] Testing reservation for non-existing product
█  # 6 [ 15ms] Testing reservation with incorrect date format
█  # 7 [ 15ms] Testing reservation with past date
█  # 8 [ 16ms] Testing reservation for product with provide_pricing=True

─────────────
BOOKING TESTS
─────────────

█  # 1 [  3ms] Booking without the reservation ID
█  # 2 [  2ms] Booking without the API key
█  # 3 [  3ms] Booking with incorrect API-Key
█  # 4 [  2ms] Booking with incorrect reservation ID.
█  # 5 [ 19ms] Booking tickets for at least 1 variant
█  # 6 [ 30ms] Perform booking that will be cancelled

───────────────
PRODUCT CATALOG
───────────────

█  # 1 [  3ms] Get product catalog
┃  Note that Tiqets will send the main booker’s name, email address and phone number with each reservation. Requiring ADDITIONAL customer data either at the order level (required_order_data ) and/or for each individual travel group member (required_visitor_data) should be done only if this is a hard requirement for the fulfillment or visitor entrance process.
```
