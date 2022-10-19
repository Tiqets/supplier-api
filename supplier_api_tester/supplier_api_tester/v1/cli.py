from supplier_api_tester.v1.exceptions import FailedTest
from supplier_api_tester.v1.printer import products_printer
from supplier_api_tester.v1.printer import results_printer
from supplier_api_tester.v1.tester import SupplierApiTesterV1
from supplier_api_tester.v1.tests.product_catalog import get_catalog


def print_title(title):
    print()
    print('-' * len(title))
    print(title)
    print('-' * len(title))
    print()


def supplier_tester(url, api_key, product_id, timeslots, availability, reservation, booking, catalog, no_colors):
    """Test your Supplier API v1.x implementation"""

    if not any((availability, reservation, booking, catalog)):
        availability = True
        reservation = True
        booking = True
        catalog = True

    if availability:
        print_title('AVAILABILITY TESTS')
        runner = SupplierApiTesterV1(
            host=url,
            api_key=api_key,
            product_id=product_id,
            test_target='availability',
            timeslots=timeslots,
        )
        results = runner.run()
        results_printer(results, no_colors)

    if reservation:
        print_title('RESERVATION TESTS')
        runner = SupplierApiTesterV1(
            host=url,
            api_key=api_key,
            product_id=product_id,
            test_target='reservation',
            timeslots=timeslots,
        )
        results = runner.run()
        results_printer(results, no_colors)

    if booking:
        print_title('BOOKING TESTS')
        runner = SupplierApiTesterV1(
            host=url,
            api_key=api_key,
            product_id=product_id,
            test_target='booking',
            timeslots=timeslots,
        )
        results = runner.run()
        results_printer(results, no_colors)

    if catalog:
        print_title('PRODUCT CATALOG')
        runner = SupplierApiTesterV1(
            host=url,
            api_key=api_key,
            product_id=product_id,
            test_target='catalog',
            timeslots=timeslots,
        )
        results = runner.run()
        results_printer(results, no_colors)


def supplier_products(url, api_key):
    """Shows the product catalog"""

    products = None
    try:
        _, products = get_catalog(url, api_key, version=1)
    except FailedTest as e:
        print(f'Unable to get the products: {e.message}')
        exit(1)

    products_printer(products)
