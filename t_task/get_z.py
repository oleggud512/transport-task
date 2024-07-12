def get_z(c: list[list[float]], plan: list[list[float | None]], real_a_count: int = None, real_b_count: int = None) -> float:
    """
    Обчислює вартість перевезень плану
    """
    res = 0
    a_count = real_a_count if real_a_count is not None else len(c)
    b_count = real_b_count if real_b_count is not None else len(c[0])
    for i in range(a_count):
        for j in range(b_count):
            if plan[i][j] is not None:
                res += c[i][j] * plan[i][j]
    return res