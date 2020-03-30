# Supplier API Testing Tool

## Requirements

Python 3.7+

## Installation

```sh
pip install supplier-api-tester
```

## Usage

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
  --help                 Show this message and exit.
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
