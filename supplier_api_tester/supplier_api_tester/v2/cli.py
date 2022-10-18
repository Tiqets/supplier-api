from supplier_api_tester.v2.exceptions import FailedTest
from supplier_api_tester.v2.printer import products_printer
from supplier_api_tester.v2.printer import results_printer
from supplier_api_tester.v2.tester import SupplierApiTester
from supplier_api_tester.v2.utils.catalog import get_catalog


def print_title(title):
    print()
    print('-' * len(title))
    print(title)
    print('-' * len(title))
    print()


def supplier_tester(url, api_key, product_id, availability, reservation, booking, catalog, no_colors):
    """Test your Supplier API implementation"""

    if not any((availability, reservation, booking, catalog)):
        availability = True
        reservation = True
        booking = True
        catalog = True

    if availability:
        print_title('AVAILABILITY TESTS')
        runner = SupplierApiTester(
            host=url,
            api_key=api_key,
            product_id=product_id,
            test_target='availability',
        )
        results = runner.run()
        results_printer(results, no_colors)

    if reservation:
        print_title('RESERVATION TESTS')
        runner = SupplierApiTester(
            host=url,
            api_key=api_key,
            product_id=product_id,
            test_target='reservation',
        )
        results = runner.run()
        results_printer(results, no_colors)

    if booking:
        print_title('BOOKING TESTS')
        runner = SupplierApiTester(
            host=url,
            api_key=api_key,
            product_id=product_id,
            test_target='booking',
        )
        results = runner.run()
        results_printer(results, no_colors)

    if catalog:
        print_title('PRODUCT CATALOG')
        runner = SupplierApiTester(
            host=url,
            api_key=api_key,
            product_id=product_id,
            test_target='catalog',
        )
        results = runner.run()
        results_printer(results, no_colors)


def supplier_products(url: str, api_key: str):
    """Shows the product catalog"""

    products = None
    try:
        print(f'Running CLI tests for API v2.x')
        _, products = get_catalog(url, api_key)
    except FailedTest as e:
        print(f'Unable to get the products: {e.message}')
        exit(1)

    products_printer(products)
