from textwrap import wrap
from typing import List
from supplier_api_tester.models import Product

from terminaltables import AsciiTable


class Colors:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def results_printer(results, no_colors=False):
    any_message = any(bool(r.message) for r in results)
    headers = ['#', 'Time', 'Test name']
    detailed_report = False
    if no_colors:
        headers.append('Result')
    if any_message:
        headers.append('Description')
    table_data = [headers]
    text_colors = {
        0: Colors.OK,
        1: Colors.WARNING,
        2: Colors.FAIL,
    }
    text_statuses = {
        0: 'OK',
        1: 'WARNINIG',
        2: 'FAIL',
    }
    for i, result in enumerate(results, 1):
        if no_colors:
            data_row = [
                i,
                f'{result.duration}ms',
                result.title,
                text_statuses[result.status],
            ]
        else:
            text_color = text_colors[result.status]
            data_row = [
                i,
                f'{text_color}{result.duration}ms{Colors.ENDC}',
                f'{text_color}{result.title}{Colors.ENDC}',
            ]
        if any_message:
            data_row.append(result.message or '')
        table_data.append(data_row)
        if not detailed_report and result.response:
            detailed_report = True
    table = AsciiTable(table_data)
    if any_message:
        columns_count = len(headers) - 1
        message_size = table.column_max_width(columns_count)
        for column in table.table_data:
            column[columns_count] = '\n'.join(wrap(column[columns_count], message_size))
    print(table.table)

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
                    print(f'{Colors.FAIL}--- #{i} {result.title} ---{Colors.ENDC}')
                    print(f'\n{Colors.WARNING}URL{Colors.ENDC}')
                    print(result.response.url)
                    print(f'\n{Colors.WARNING}STATUS_CODE{Colors.ENDC}')
                    print(result.response.status_code)
                    print(f'\n{Colors.WARNING}HEADERS{Colors.ENDC}')
                    for header, value in result.response.headers.items():
                        print(f'{header}: {value}')
                    print(f'\n{Colors.WARNING}PAYLOAD{Colors.ENDC}')
                    print(result.response.payload)
                    print(f'\n{Colors.WARNING}RESPONSE{Colors.ENDC}')
                    print(result.response.body)
                print()


def products_printer(products: List[Product]) -> None:
    rows = [['ID', 'Name', 'Timeslots', 'Refundable', 'Cutoff time']]
    rows.extend([
        [
            p.id,
            p.name,
            p.use_timeslots,
            p.is_refundable,
            p.cutoff_time,
        ] for p in products]
    )
    table = AsciiTable(rows)
    print(table.table)
