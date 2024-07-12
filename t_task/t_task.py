from dataclasses import dataclass

from t_task.get_next_plan import get_next_plan
from t_task.get_potentials import get_potentials
from t_task.get_pseudo_c import get_pseudo_c
from t_task.get_z import get_z
from t_task.north_west import north_west
from t_task.print_t_table import print_t_table


@dataclass
class TTaskResult:
    plan: list[list[float | None]]
    total_cost: float


def t_task(a: list[float], b: list[float], c: list[list[float]]) -> TTaskResult:
    """
    Вирішення транспортної задачі методом північно-західного кута та методом потенціалів.
    """
    assert(len(c) == len(a) and len(c[0]) == len(b))

    sum_a = sum(a)
    sum_b = sum(b)
    
    temp_a = [*a]
    temp_b = [*b]
    temp_c = [[cell for cell in row] for row in c]

    if sum_a > sum_b:
        temp_b.append(sum_a - sum_b)
        temp_c = [[*row, 0] for row in temp_c]
    elif sum_a < sum_b:
        temp_a.append(sum_b - sum_a)
        temp_c.append([0 for _ in range(len(temp_c))])
    
    cur_temp_plan = north_west(temp_c, temp_a, temp_b)
    print_t_table(temp_c, temp_a, temp_b)
    print("north west:")
    print_t_table(cur_temp_plan, temp_a, temp_b)
    i = 0
    while True:
        print(f"  ITER {i}")
        i += 1
        u, v = get_potentials(temp_c, cur_temp_plan)
        c_ps = get_pseudo_c(temp_c, cur_temp_plan, u, v)
        print("plan: ")
        print_t_table(cur_temp_plan, temp_a, temp_b, u, v)
        print("pseudo c:")
        print_t_table(c_ps, temp_a, temp_b, u, v)
        print(f"current z = {get_z(temp_c, cur_temp_plan)} (real z = {get_z(temp_c, cur_temp_plan, len(a), len(b))})")
        next_temp_plan = get_next_plan(temp_c, cur_temp_plan, c_ps, u, v)
        
        if next_temp_plan is None:
            break
        else:
            cur_temp_plan = next_temp_plan
    
    plan = cur_temp_plan
    if sum_a > sum_b:
        plan = [row[:-1] for row in cur_temp_plan]
    elif sum_a < sum_b:
        plan = [row for i, row in enumerate(cur_temp_plan) if i != len(cur_temp_plan)-1]

    return TTaskResult(plan, get_z(c, plan))