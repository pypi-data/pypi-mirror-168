from typing import Any, Callable, Final, Sequence, Tuple, TypeVar

import colorama
from prettytable import PrettyTable

from beni import bcolor

_T = TypeVar('_T')


def get(
    data_list: Sequence[_T],
    *,
    title: str | None = None,
    fields: Sequence[Tuple[str, Callable[[_T], Any]]],
    rowcolor: Callable[[list[Any]], Any] | None = None,
    extend: list[list[Any]] | None = None,
    isPrint: bool = False,
):
    header_color: Final = colorama.Fore.YELLOW
    table = PrettyTable()
    if title:
        table.title = bcolor.getStr(title, header_color)
    field_funclist: list[Callable[[_T], Any]] = []
    field_namelist: list[str] = []
    align_dict: dict[str, str] = {}
    for i in range(len(fields)):
        item = fields[i]
        field_funclist.append(item[1])
        field_name = item[0]
        if field_name.endswith('>'):
            field_name = field_name[:-1]
            align_dict[field_name] = 'r'
        elif field_name.endswith('<'):
            field_name = field_name[:-1]
            align_dict[field_name] = 'l'
        field_namelist.append(field_name)
    table.field_names = [bcolor.getStr(x, header_color) for x in field_namelist]
    for k, v in align_dict.items():
        table.align[bcolor.getStr(k, header_color)] = v
    row_list: list[list[Any]] = []
    for data in data_list:
        row = [func(data) for func in field_funclist]
        row_list.append(row)
    if extend:
        for row in extend:
            newRow = row[:]
            if len(newRow) < len(fields):
                newRow.extend([''] * (len(fields) - len(newRow)))
            row_list.append(newRow)
    if rowcolor:
        for row in row_list:
            color = rowcolor(row)
            if color:
                for i in range(len(row)):
                    row[i] = bcolor.getStr(row[i], color)
    table.add_rows(row_list)
    tableStr = str(table.get_string())
    if isPrint:
        print(f'\n{tableStr}\n')
    return tableStr
