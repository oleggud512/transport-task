from typing import Callable
import tabulate


def print_t_table(
        c: list[list[float | None]], 
        a: list[float], 
        b: list[float], 
        u: list[float] | None = None, 
        v: list[float] | None = None,
        create_a_alias: Callable[[int], str] | None = None,
        create_b_alias: Callable[[int], str] | None = None,
        ):
    """
    Виводить дані задачі в термінал.
    """
    assert(u is None and v is None or u is not None and v is not None)
    create_a_alias = create_a_alias if create_a_alias else lambda i: f"A_{i+1}"
    create_b_alias = create_b_alias if create_b_alias else lambda j: f"B_{j+1}"

    v_rows = []
    b_head_row = [ "", "", *[create_b_alias(j) for j in range(len(b))] ]
    b_row = [ "", "", *[bj for bj in b] ]
    

    if u is not None:
        b_head_row.insert(0, "")
        b_row.insert(0, "")
        v_rows.append(["", "", "", *[f"v{j+1} = {v[j]}" for j in range(len(v))]])

    a_rows = []
    for i in range(len(a)):
        a_row = [ create_a_alias(i), a[i], *c[i] ]
        if u is not None:
            a_row.insert(0, f"u{i+1} = {u[i]}")
        a_rows.append(a_row)

    res = tabulate.tabulate(
        tabular_data=[
            *v_rows,
            b_head_row,
            b_row,
            *a_rows
        ],
        tablefmt="grid",
        numalign="center",
        stralign="center"
    )
    print(res)