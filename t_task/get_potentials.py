def plan_to_graph(plan: list[list[float | None]]) -> dict[tuple[int, int], list[tuple[int, int]]]:
    graph: dict[tuple[int, int], list[tuple[int, int]]] = dict()

    for i in range(len(plan)):
        for j in range(len(plan[i])):
            if plan[i][j] is not None:
                neighbours = []
                for ii in range(len(plan)):
                    if plan[ii][j] is not None and ii != i:
                        neighbours.append((ii, j))
                for jj in range(len(plan[i])):
                    if plan[i][jj] is not None and jj != j:
                        neighbours.append((i, jj))
                graph[(i, j)] = neighbours
    return graph


def set_potentials_recursive(
        c: list[list[float | None]], 
        plan: list[list[float | None]],
        visited: set[tuple[int, int]],
        graph: dict[tuple[int, int], list[tuple[int, int]]],
        u: list[float | None], 
        v: list[float | None], 
        node: tuple[int, int]
):
    if node not in visited:
        i, j = node
        if u[i] is not None and v[j] is not None:
            ...
        elif u[i] is not None:
            v[j] = c[i][j] - u[i]
            print(f"v_{j+1} = c_{i+1}{j+1} - u_{i+1} = {c[i][j]} - {u[i]} = {c[i][j] - u[i]}")
        elif v[j] is not None:
            u[i] = c[i][j] - v[j]
            print(f"u_{i+1} = c_{i+1}{j+1} - v_{j+1} = {c[i][j]} - {v[j]} = {c[i][j] - v[j]}")
        visited.add(node)

        for neighbour in graph[node]:
            set_potentials_recursive(c, plan, visited, graph, u, v, neighbour)


def get_potentials(c: list[list[float]], plan: list[list[float | None]]) -> tuple[list[float], list[float]]:
    """
    Знаходить значення потенціалів базисних змінних.
    """
    graph = plan_to_graph(plan)
    visited = set()
    u = [0, *[None for _ in range(len(c)-1)]]
    v = [None for _ in range(len(c[0]))]
    node = (0, 0)
    for j in range(len(plan[0])):
        if plan[0][j] is not None:
            node = (0, j)
    print("getting potentials")
    set_potentials_recursive(c, plan, visited, graph, u, v, node)
    print("end getting potentials")
    print(f"got pot: {(u, v)}")
    return u, v