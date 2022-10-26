import click

from supplier_api_tester.v2.cli import supplier_tester as supplier_tester_v2
from supplier_api_tester.v2.cli import supplier_products as supplier_products_v2

from supplier_api_tester.v1.cli import supplier_tester as supplier_tester_v1
from supplier_api_tester.v1.cli import supplier_products as supplier_products_v1


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
@click.option('-v', '--version', default=2, help='Choosing the API version', prompt='API version', type=int)
def supplier_tester(
        url, api_key, product_id, timeslots, availability, reservation, booking, catalog, no_colors, version: int
):
    """Test your Supplier API implementation"""

    if not any((availability, reservation, booking, catalog)):
        availability = True
        reservation = True
        booking = True
        catalog = True

    if any((availability, timeslots, reservation, booking)) and not product_id:
        product_id = click.prompt('Product ID')

    if version == 1:
        supplier_tester_v1(url, api_key, product_id, timeslots, availability, reservation, booking, catalog, no_colors)
    else:
        supplier_tester_v2(url, api_key, product_id, availability, reservation, booking, catalog, no_colors)


@click.command()
@click.option('-u', '--url', required=True, prompt='Server URL', type=str)
@click.option('-k', '--api-key', required=True, prompt='API Key', type=str)
@click.option('-v', '--version', default=2, help='Choosing the API version', prompt='API version', type=int)
def supplier_products(url: str, api_key: str, version: int):
    """Shows the product catalog"""

    if version == 1:
        supplier_products_v1(url, api_key)
    else:
        supplier_products_v2(url, api_key)
