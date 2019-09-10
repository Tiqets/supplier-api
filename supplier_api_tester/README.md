# Supplier API Testing Tool

## Requirements

Python 3.6+

## Usage

```
supplier_tester --help
Usage: supplier_tester [OPTIONS]

  Test you Supplier API implementation

Options:
  -u, --url TEXT         [required]
  -k, --api-key TEXT     [required]
  -p, --product-id TEXT  [required]
  -t, --timeslots
  -a, --availability
  -r, --reservation
  -b, --booking
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
