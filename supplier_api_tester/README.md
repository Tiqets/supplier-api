# Supplier API Testing Tool

## Requirements

Python 3.7+

## Installation

```sh
pip install supplier-api-tester
```

## Usage

Listing the products catalog:

```sh
supplier_products -u 'http://localhost:8000' -k 'secret'
+---------+---------+-----------+------------+-------------+
| ID      | Name    | Timeslots | Refundable | Cutoff time |
+---------+---------+-----------+------------+-------------+
| A300-FX | A300-FX | True      | True       | 24          |
| A400-FX | A400-FX | True      | False      | 0           |
| A500-FX | A500-FX | False     | True       | 0           |
| A550-FX | A550-FX | False     | True       | 10          |
| A600-FX | A600-FX | False     | False      | 0           |
+---------+---------+-----------+------------+-------------+
```

Testing tool usage:
```
supplier_tester --help
Usage: supplier_tester [OPTIONS]

  Test you Supplier API implementation

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
  --help                 Show this message and exit
```

Running all tests:

```sh
    supplier_tester -u 'http://localhost:8000' -k 'secret' -p 'A500-FX'  # For products without timeslots
    supplier_tester -u 'http://localhost:8000' -k 'secret' -p 'A400-FX' -t  # For products with timeslots
```

**Remember to choose valid product id. It has to refer timeslotted product when you use `-t` flag.**

Running only availability tests:

```sh
    supplier_tester -u 'http://localhost:8000' -k 'secret' -p 'A500-FX' -a  # For products without timeslots
    supplier_tester -u 'http://localhost:8000' -k 'secret' -p 'A400-FX' -a -t  # For products with timeslots
```

Test example:

```sh
supplier_tester -u 'http://localhost:8000' -k 'secret' -p 'A500-FX'

------------------
AVAILABILITY TESTS
------------------

+----+------+--------------------------------------------------------------+----------------------------+
| #  | Time | Test name                                                    | Description                |
+----+------+--------------------------------------------------------------+----------------------------+
| 1  | 5ms  | [Variants] Checking response format                          |                            |
| 2  | 10ms | [Variants] Checking for any availability in the next 30 days |                            |
| 3  | 3ms  | [Variants] Request without API-Key                           |                            |
| 4  | 3ms  | [Variants] Request with incorrect API-Key                    |                            |
| 5  | 10ms | [Variants] Testing missing argument errors                   |                            |
| 6  | 3ms  | [Variants] Testing availability for non existing product     |                            |
| 7  | 6ms  | [Variants] Checking incorrect date format                    |                            |
| 8  | 3ms  | [Variants] Checking incorrect range error                    |                            |
| 9  | 4ms  | [Variants] Checking past date                                |                            |
| 10 | 3ms  | [Variants] Checking huge date range                          |                            |
| 11 | 3ms  | [Variants] Checking empty availability                       | Skipping that test because |
|    |      |                                                              | response is not empty.     |
| 12 | 14ms | [Variants] Testing methods that are not allowed              |                            |
| 13 | 3ms  | [Timeslots] Testing errors on invalid (non-timeslot) product |                            |
+----+------+--------------------------------------------------------------+----------------------------+

-----------------
RESERVATION TESTS
-----------------

+---+------+------------------------------------------------+
| # | Time | Test name                                      |
+---+------+------------------------------------------------+
| 1 | 3ms  | Request without API-Key                        |
| 2 | 4ms  | Request with incorrect API-Key                 |
| 3 | 21ms | Testing missing argument errors                |
| 4 | 3ms  | Reserving tickets for at least 1 variant       |
| 5 | 4ms  | Testing reservation for non-existing product   |
| 6 | 4ms  | Testing reservation with incorrect date format |
| 7 | 3ms  | Testing reservation with past date             |
| 8 | 13ms | Testing methods that are not allowed           |
+---+------+------------------------------------------------+

-------------
BOOKING TESTS
-------------

+---+------+----------------------------------------+
| # | Time | Test name                              |
+---+------+----------------------------------------+
| 1 | 4ms  | Booking without the reservation ID     |
| 2 | 2ms  | Booking without the API key            |
| 3 | 4ms  | Booking with incorrect API-Key         |
| 4 | 13ms | Testing methods that are not allowed   |
| 5 | 3ms  | Booking with incorrect reservation ID. |
| 6 | 7ms  | Booking tickets for at least 1 variant |
| 7 | 21ms | Perform booking that will be cancelled |
+---+------+----------------------------------------+

---------------
PRODUCT CATALOG
---------------

+---+------+-----------------------------------------------------------+
| # | Time | Test name                                                 |
+---+------+-----------------------------------------------------------+
| 1 | 4ms  | Get product catalog                                       |
| 2 | 3ms  | Get product catalog with use_timeslots=True query filter  |
| 3 | 3ms  | Get product catalog with use_timeslots=False query filter |
+---+------+-----------------------------------------------------------+
```
