from typing import List
from .models import Product


class Color:
    OK = '\033[92m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    GRAY = '\033[90m'


def results_printer(results, no_colors=False):
    detailed_report = False
    text_colors = {
        0: Color.OK,
        1: Color.WARNING,
        2: Color.FAIL,
    }
    text_statuses = {
        0: 'OK',
        1: 'WARNINIG',
        2: 'FAIL',
    }
    for i, result in enumerate(results, 1):
        if no_colors:
            print(f'{text_statuses[result.status]}  #{str(i).rjust(2, " ")} [{str(result.duration).rjust(3, " ")}ms] {result.title}')
            if result.message:
                print(f'┃  {result.message}')
        else:
            text_color = text_colors[result.status]
            print(f'{text_color}█  #{str(i).rjust(2, " ")} [{str(result.duration).rjust(3, " ")}ms] {result.title}{Color.END}')
            if result.message:
                print(f'{text_color}┃  {result.message}{Color.END}')
        if not detailed_report and result.response:
             detailed_report = True

    if detailed_report:
        print('\nREPORTS FROM FAILED TESTS\n')
        for i, result in enumerate(results, 1):
            if result.response:
                if no_colors:
                    print(f'--- #{i} {result.title} ---')
                    print('\nURL')
                    print(result.response.url)
                    print('\nSTATUS_CODE')
                    print(result.response.status_code)
                    print('\nHEADERS')
                    for header, value in result.response.headers.items():
                        print(f'{header}: {value}')
                    print('\nPAYLOAD')
                    print(result.response.payload)
                    print('\nRESPONSE')
                    print(result.response.body)
                else:
                    print(f'{Color.FAIL}--- #{i} {result.title} ---{Color.END}')
                    print(f'\n{Color.WARNING}URL{Color.END}')
                    print(result.response.url)
                    print(f'\n{Color.WARNING}STATUS_CODE{Color.END}')
                    print(result.response.status_code)
                    print(f'\n{Color.WARNING}HEADERS{Color.END}')
                    for header, value in result.response.headers.items():
                        print(f'{header}: {value}')
                    print(f'\n{Color.WARNING}PAYLOAD{Color.END}')
                    print(result.response.payload)
                    print(f'\n{Color.WARNING}RESPONSE{Color.END}')
                    print(result.response.body)
                print()


def pdetail(key: str, value: str):
    value_str = value
    if isinstance(value, bool):
        value_str = 'yes' if value else 'no' 
    print(f'{Color.GRAY}{key}:{Color.END} {value_str}')

def products_printer(products: List[Product]) -> None:
    for p in products:
        print(f'{Color.GREEN}{p.name}{Color.END}')
        pdetail('ID', p.id)
        pdetail('Timeslots', p.use_timeslots)
        pdetail('Refundable', p.is_refundable)
        pdetail('Cutoff time', p.cutoff_time)
        print('')
    print(f'Products found: {len(products)}')
