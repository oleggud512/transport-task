
from input_utils import input_list, input_matrix, try_float, try_int
from t_task.print_t_table import print_t_table
from t_task.t_task import t_task

a_count = try_int(input("Введіть кількість постачальників:\n"))
b_count = try_int(input("Введіть кількість споживачів:\n"))

print("Введіть назви постачальників:")
a_names: list[str] = input_list(
    a_count, 
    create_message=lambda i: f"{i+1}: ", 
    )

print("Введіть назви споживачів:")
b_names: list[str] = input_list(
    b_count, 
    create_message=lambda i: f"{i+1}: "
    )

print("Введіть кількість товарів, що має кожен постачальник:")
a: list[float] = input_list(
    a_count,
    create_message=lambda i: f"{a_names[i]}: ",
    parser=try_float
)
print("Введіть кількість товарів що необхідна кожному із споживачів:")
b: list[float] = input_list(
    b_count,
    create_message=lambda i: f"{b_names[i]}: ",
    parser=try_float
)

print("Введіть оціночні вартості перевезення товару від кожного\nпостачальника до кожного споживача:")
c: list[list[float]] = input_matrix(
    height=a_count,
    width=b_count,
    create_row_message=lambda row_i: f"{a_names[row_i]}: ",
    create_cell_message=lambda col_i: f"{b_names[col_i]}: ",
    parser=try_float
)

print("Введення даних завершено.\nВхідні дані задачі:")
print_t_table(
    c, 
    a, 
    b,
    create_a_alias=lambda i: a_names[i],
    create_b_alias=lambda j: b_names[j]
    )

res = t_task(a, b, c)

print("Оптимальний план перевезень (ов - одиниць вантажу):")
for i in range(len(res.plan)):
    print(f"  Постачальник \"{a_names[i]}\" відправляє ", end="")
    spare = a[i]
    mes_parts = []
    for j in range(len(res.plan[i])):
        if res.plan[i][j] is not None and res.plan[i][j] != 0:
            mes_parts.append(f"{res.plan[i][j]} ов споживачу \"{b_names[j]}\"")
            spare -= res.plan[i][j]
    mes = ", ".join(mes_parts)
    print(mes, end="")
    if spare > 0:
        print(f" і {spare} ов залишиться в ного", end="")
    print('.')

print(f"Загальна вартість такого плану перевезень складає {res.total_cost}.")