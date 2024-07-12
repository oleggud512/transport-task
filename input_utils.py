from typing import Any, Callable


def try_float(s: str) -> float:
    try:
        return float(s)
    except ValueError:
        return 0.0


def try_int(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        return 0


def input_list(
        length: int, 
        create_message: Callable[[int], Any] | None = None, 
        parser: Callable[[str], Any] | None = None
        ) -> list:
    res = []
    create_message = create_message if create_message else lambda i: f"{i}: "
    parser = parser if parser else lambda s: s
    for i in range(length):
        item = input(create_message(i))
        res.append(parser(item))
    return res


def input_matrix(
        height: int, 
        width: int, 
        create_row_message: Callable[[int], Any] | None = None, 
        create_cell_message: Callable[[int], Any] | None = None, 
        parser: Callable[[str], Any] | None = None
        ) -> list[list]:
    row_msg = create_row_message if create_row_message else lambda i: f"{i}:"
    cell_msg = lambda i: f"    {create_cell_message(i)}" if create_cell_message else lambda i: f"    {i}: "
    res = []
    for i in range(height):
        print(row_msg(i))
        row = input_list(width, cell_msg, parser)
        res.append(row)
    return res
