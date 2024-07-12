def get_pseudo_c(c: list[list[float]], plan: list[list[float | None]], u: list[float], v: list[float]) -> list[list[float | None]]:
    """
    Повертає псевдо тарифи небазисних змінних. `None` для базисних.
    """
    print("getting pseudo c")
    c_ps = []

    for i in range(len(c)):
        c_ps.append([])
        for j in range(len(c[i])):
            if plan[i][j] is not None:
                c_ps[i].append(None)
                continue
            c_ps[i].append(c[i][j] - (u[i] + v[j]))
            print(f"c_{i+1}{j+1}' = c_{i+1}{j+1} - (u_{i+1} + v{j+1}) = {c[i][j]} - ({u[i]} + {v[j]}) = {c[i][j] - (u[i] + v[j])}")
    print('end getting pseudo c')
    return c_ps