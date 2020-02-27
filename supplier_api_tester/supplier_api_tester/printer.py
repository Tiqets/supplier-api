from textwrap import wrap

from terminaltables import AsciiTable


class Colors:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def terminal_printer(results):
    any_message = any(bool(r.message) for r in results)
    headers = ['#', 'Time', 'Test name']
    if any_message:
        headers.append('Description')
    table_data = [headers]
    for i, result in enumerate(results, 1):
        text_color = {
            0: Colors.OK,
            1: Colors.WARNING,
            2: Colors.FAIL,
        }[result.status]
        data_row = [
            i,
            f'{text_color}{result.duration}ms{Colors.ENDC}',
            f'{text_color}{result.title}{Colors.ENDC}',
        ]
        if any_message:
            data_row.append(result.message or '')
        table_data.append(data_row)
    table = AsciiTable(table_data)
    if any_message:
        message_size = table.column_max_width(3)
        for column in table.table_data:
            column[3] = '\n'.join(wrap(column[3], message_size))
    print(table.table)
