from textwrap import wrap

from terminaltables import AsciiTable


class Colors:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def terminal_printer(results, no_colors=False):
    any_message = any(bool(r.message) for r in results)
    headers = ['#', 'Time', 'Test name']
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
    table = AsciiTable(table_data)
    if any_message:
        columns_count = len(headers) - 1
        message_size = table.column_max_width(columns_count)
        for column in table.table_data:
            column[columns_count] = '\n'.join(wrap(column[columns_count], message_size))
    print(table.table)
