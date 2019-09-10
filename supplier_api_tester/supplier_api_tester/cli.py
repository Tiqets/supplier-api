import click

from supplier_api_tester.tester import SupplierApiTester
from supplier_api_tester.printer import terminal_printer


def print_title(title):
    print()
    print('-' * len(title))
    print(title)
    print('-' * len(title))
    print()


@click.command()
@click.option('-u', '--url', required=True, prompt='Server URL', type=str)
@click.option('-k', '--api-key', required=True, prompt='API Key', type=str)
@click.option('-p', '--product-id', required=True, prompt='Product ID', type=str)
@click.option('-t', '--timeslots', is_flag=True, default=False, help='Use timeslots')
@click.option('-a', '--availability', is_flag=True, default=False, help='Run availability tests')
@click.option('-r', '--reservation', is_flag=True, default=False, help='Run reservation tests')
@click.option('-b', '--booking', is_flag=True, default=False, help='Run booking tests')
def supplier_tester(url, api_key, product_id, timeslots, availability, reservation, booking):
    '''Test you Supplier API implementation'''
    if not any((availability, reservation, booking)):
        availability = True
        reservation = True
        booking = True

    if availability:
        print_title('AVAILABILITY TESTS')
        runner = SupplierApiTester(
            host=url,
            api_key=api_key,
            product_id=product_id,
            availability_test=True,
            reservation_test=False,
            booking_test=False,
            timeslots=timeslots,
        )
        results = runner.run()
        terminal_printer(results)

    if reservation:
        print_title('RESERVATION TESTS')
        runner = SupplierApiTester(
            host=url,
            api_key=api_key,
            product_id=product_id,
            availability_test=False,
            reservation_test=True,
            booking_test=False,
            timeslots=timeslots,
        )
        results = runner.run()
        terminal_printer(results)

    if booking:
        print_title('BOOKING TESTS')
        runner = SupplierApiTester(
            host=url,
            api_key=api_key,
            product_id=product_id,
            availability_test=False,
            reservation_test=False,
            booking_test=True,
            timeslots=timeslots,
        )
        results = runner.run()
        terminal_printer(results)
