import tabulate
from .cycle import get_cycle


def get_next_plan(
        c: list[list[float]], 
        plan: list[list[float | None]], 
        c_ps: list[list[float | None]], 
        u: list[float], 
        v :list[float]
        ) -> list[list[float | None]] | None:
    """
    Повртає оновлений план.
    Якщо жоден з циклів не змінює план, або якщо цикл не знайдено (немає від'ємних псевдо тарифів), повертає `None`.
    """
    print("while creating next plan")
    # зберігає індекси негативних небазисних елементів
    c_ps_neg: list[tuple[int, int]] = []
    for i in range(len(c_ps)):
        for j in range(len(c_ps[i])):
            if c_ps[i][j] is not None and c_ps[i][j] < 0:
                c_ps_neg.append((i, j))
    
    # якщо негативних псевдо тарифів немає, то шукти наступний план не потрібно
    if len(c_ps_neg) == 0:
        print("congrats. u+v <= c для кожного!")
        return None
    
    # сортування за зменшенням значення псевдо тарифу та зменшенням значення тарифу
    c_ps_neg = sorted(c_ps_neg, key=lambda ij: (c_ps[ij[0]][ij[1]], c[ij[0]][ij[1]]))

    new_plan: list[list[float | None]] = None
    while new_plan is None and len(c_ps_neg) > 0:
        print(f"candidate: {[(i+1, j+1) for i, j in c_ps_neg]}")
        lead_cell = c_ps_neg.pop(0)
        print(f"cur lead: {(lead_cell[0]+1, lead_cell[1]+1)}")
        cur_cycle_cells = get_cycle(plan, lead_cell)
        print(tabulate.tabulate(
            tabular_data=[
                ["cur_cycle", *[(i+1, j+1) for i, j in cur_cycle_cells]],
                ["cur_cycle values", *[plan[i][j] for i, j in cur_cycle_cells]]
            ]
        ))
        min_minus_value = min([plan[i][j] for cell_i, (i, j) in enumerate(cur_cycle_cells[1:]) if cell_i % 2 == 0])
        print(f"min min: {min_minus_value}")
        # якщо значення зсуву дорівнює 0, то обираємо наступний цикл
        if min_minus_value == 0:
            print("it's zero. try again")
            continue
        
        # оновлення значеннь у вершинах циклу
        new_plan = [[cell for cell in row] for row in plan]
        for cell_i, (i, j) in enumerate(cur_cycle_cells):
            dx = -min_minus_value if cell_i % 2 != 0 else min_minus_value
            if new_plan[i][j] is None:
                new_plan[i][j] = dx
            else:
                new_plan[i][j] += dx
        
        # виведення з базису нульового план що має найбільший тариф
        non_base_cell = max([cell for cell in cur_cycle_cells if new_plan[cell[0]][cell[1]] == 0], key=lambda cell: c[cell[0]][cell[1]])
        print(f"excluded zero: {non_base_cell}")
        new_plan[non_base_cell[0]][non_base_cell[1]] = None
    print("end creating next plan")
    return new_plan