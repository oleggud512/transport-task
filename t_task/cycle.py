import tabulate

def oposite_dir(dir: str) -> str:
    """
    Зміна напрямку пошуку на 180.
    """
    dir_map = {
        'r': 'l',
        'l': 'r',
        'u': 'd',
        'd': 'u'
    }
    return dir_map[dir]


def oposite_axis(dir: str) -> str:
    """
    Зміна напрямку пошуку на 90 чи 270 градусів.
    """
    dir_map = {
        'r': 'd',
        'l': 'd',
        'u': 'r',
        'd': 'r'
    }
    return dir_map[dir]


def translate(point: tuple[int, int], direction: int) -> tuple[int, int]:
    """
    Зміна координат клітини на основі напрямку руху.
    """
    if direction == "r":
        next = (point[0], point[1]+1)
    if direction == "l":
        next = (point[0], point[1]-1)
    if direction == "u":
        next = (point[0]-1, point[1])
    if direction == "d":
        next = (point[0]+1, point[1])
    return next


def cycle_recursive(
        plan: list[list[float | None]],
        start: tuple[int, int],
        cur: tuple[int, int],
        prev: tuple[int, int] = None,
        direction: str = "r"
) -> list[tuple[int, int]]:
    # print_cur(plan, cur)
    # input()
    next_pos = translate(cur, direction)
    if cur[0] >= len(plan) or cur[0] < 0 or cur[1] >= len(plan[0]) or cur[1] < 0:
        return []
        
    
    if start != cur and plan[cur[0]][cur[1]] is not None:
        dir90 = oposite_axis(direction)
        nodes90 = cycle_recursive(plan, start, translate(cur, dir90), cur, dir90)
        if len(nodes90) > 0:
            return [cur, *nodes90]
        
        dir270 = oposite_dir(dir90)
        nodes270 = cycle_recursive(plan, start, translate(cur, dir270), cur, dir270)
        if len(nodes270) > 0:
            return [cur, *nodes270]
        
        # продовження руху у тому самому напрямку та пропуск поточної базисної клітини
        if next_pos[0] < len(plan) and next_pos[0] >= 0 and next_pos[1] < len(plan[0]) and next_pos[1] >= 0:
            return cycle_recursive(plan, start, next_pos, prev, direction)
        
        return []
    
    elif start == cur and prev is not None:
        # цикл знайдено. Завершення циклу.
        return [start]
    
    if next_pos[0] >= len(plan) or next_pos[0] < 0 or next_pos[1] >= len(plan[0]) or next_pos[1] < 0:
        # якщо наступний елемент (не важливо, базисний чи не базисний)
        # виходить за межі, та ніяких інших елементів циклу ще не знайдено, 
        # то змінюємо напрямок пошуку на протилежний
        if prev is None:
            dir180 = oposite_dir(direction)
            return cycle_recursive(plan, start, translate(cur, dir180), prev, dir180)
        return []
    return cycle_recursive(plan, start, next_pos, prev, direction)


def get_cycle(plan: list[list[float]], start: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Повертає цикл на основі небазисної клітини
    """
    i, j = start

    directions = ["l", "r", "u", "d"]
    for direction in directions:
        cycle = cycle_recursive(plan, (i, j), (i, j), None, direction)
        if cycle:
            return list(reversed(cycle))

    return []

def print_cur(plan: list[list[float | None]], cur: tuple[int, int]):
    """
    Виведення поточного стану циклу.
    """
    res = []
    for i in range(len(plan)):
        row = []
        for j in range(len(plan[i])):
            if plan[i][j] is None:
                if (i, j) == cur:
                    row.append("-(-)-")
                else:
                    row.append("-----")
            else:
                if (i, j) == cur:
                    row.append(f"({plan[i][j]})")
                else:
                    row.append(plan[i][j]) 
        res.append(row)
    print(tabulate.tabulate(
        tabular_data=res,
        tablefmt="grid",
        stralign="center",
        numalign="center"
    ))