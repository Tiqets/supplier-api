import click

from .exceptions import FailedTest  # generic for v1 and v2

from .tester import SupplierApiTester
from .printer import results_printer
from .printer import products_printer
from .utils.catalog import get_catalog

from supplier_api_tester.v1.tester import SupplierApiTesterV1
from supplier_api_tester.v1.tests.product_catalog import get_catalog as get_catalog_v1
from supplier_api_tester.v1.printer import results_printer as results_printer_v1
from supplier_api_tester.v1.printer import products_printer as products_printer_v1


def print_title(title):
    print()
    print('-' * len(title))
    print(title)
    print('-' * len(title))
    print()


@click.command()
@click.option('-u', '--url', required=True, prompt='Server URL', type=str)
@click.option('-k', '--api-key', required=True, prompt='API Key', type=str)
@click.option('-p', '--product-id', type=str, help='Product ID to call tests on. Required with -a and -t flags')
@click.option('-t', '--timeslots', is_flag=True, default=False, help='Use timeslots. Not supported in v2.x')
@click.option('-a', '--availability', is_flag=True, default=False, help='Run availability tests')
@click.option('-r', '--reservation', is_flag=True, default=False, help='Run reservation tests')
@click.option('-b', '--booking', is_flag=True, default=False, help='Run booking tests')
@click.option('-c', '--catalog', is_flag=True, default=False, help='Run product catalog tests')
@click.option('-nc', '--no-colors', is_flag=True, default=False, help='Not using colors on output')
@click.option('-v1', '--version-1', is_flag=True, default=False, help='Run the CLI tests for API v1.x')
def supplier_tester(
        url, api_key, product_id, timeslots, availability, reservation, booking, catalog, no_colors, version_1: bool
):
    """Test your Supplier API implementation"""

    if not any((availability, reservation, booking, catalog)):
        availability = True
        reservation = True
        booking = True
        catalog = True

    if any((availability, timeslots, reservation, booking)) and not product_id:
        product_id = click.prompt('Product ID')

    if availability:
        print_title('AVAILABILITY TESTS')
        if version_1:
            runner = SupplierApiTesterV1(
                host=url,
                api_key=api_key,
                product_id=product_id,
                test_target='availability',
                timeslots=timeslots,
            )
            results = runner.run()
            results_printer_v1(results, no_colors)
        else:
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
        if version_1:
            runner = SupplierApiTesterV1(
                host=url,
                api_key=api_key,
                product_id=product_id,
                test_target='reservation',
                timeslots=timeslots,
            )
            results = runner.run()
            results_printer_v1(results, no_colors)
        else:
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
        if version_1:
            runner = SupplierApiTesterV1(
                host=url,
                api_key=api_key,
                product_id=product_id,
                test_target='booking',
                timeslots=timeslots,
            )
            results = runner.run()
            results_printer_v1(results, no_colors)
        else:
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
        if version_1:
            runner = SupplierApiTesterV1(
                host=url,
                api_key=api_key,
                product_id=product_id,
                test_target='catalog',
                timeslots=timeslots,
            )
            results = runner.run()
            results_printer_v1(results, no_colors)
        else:
            runner = SupplierApiTester(
                host=url,
                api_key=api_key,
                product_id=product_id,
                test_target='catalog',
            )
            results = runner.run()
            results_printer(results, no_colors)


@click.command()
@click.option('-u', '--url', required=True, prompt='Server URL', type=str)
@click.option('-k', '--api-key', required=True, prompt='API Key', type=str)
@click.option('-v1', '--version-1', is_flag=True, default=False, help='Run the CLI testing tools for API v1.x')
def supplier_products(url: str, api_key: str, version_1: bool):
    """Shows the product catalog"""
    try:
        if version_1:
            print(f'Running CLI tests for API v1.x')
            _, products = get_catalog_v1(url, api_key, version=1)
        else:
            print(f'Running CLI tests for API v2.x')
            _, products = get_catalog(url, api_key)
    except FailedTest as e:
        print(f'Unable to get the products: {e.message}')
        exit(1)

    if version_1:
        products_printer_v1(products)
    else:
        products_printer(products)
