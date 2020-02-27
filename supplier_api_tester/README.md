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
  -p, --product-id TEXT  [required]
  -t, --timeslots        Use timeslots
  -a, --availability     Run availability tests
  -r, --reservation      Run reservation tests
  -b, --booking          Run booking tests
  -c, --catalog          Run product catalog tests
  --help                 Show this message and exit.
```

Running all tests:

```sh
    supplier_tester -u 'http://localhost:8000' -k 'secret' -p 'A400-FX'
```

Running only availability tests:

```sh
    supplier_tester -u 'http://localhost:8000' -k 'secret' -p 'A400-FX' -a
```
