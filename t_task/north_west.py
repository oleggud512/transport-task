from .t_exception import TException

def north_west(c: list[list[float]], a: list[float], b: list[float]) -> list[list[float | None]]:
    """
    Створює опорний план методом північно західного кута. `None` для небазисних планів.
    """
    plan: list[list[float | None]] = [[None for _ in row] for row in c]

    _a = [*a]
    _b = [*b]
    i = 0
    j = 0

    while i < len(c) and j < len(c[0]):
        dai = None
        dbj = None
        di = 0
        dj = 0

        if _a[i] < _b[j]:
            plan[i][j] = _a[i]
            dai = 0
            dbj = _b[j] - _a[i]
            di = 1

        elif _a[i] > _b[j]:
            plan[i][j] = _b[j]
            dai = _a[i] - _b[j]
            dbj = 0
            dj = 1

        elif _a[i] == _b[j]:
            plan[i][j] = _a[i]
            dai = 0
            dbj = 0
            di = 1
            dj = 1
            
            if i+1 < len(c) and j+1 < len(c[i]):
                if c[i+1][j] < c[i][j+1]:
                    plan[i+1][j] = 0
                elif c[i+1][j] > c[i][j+1]:
                    plan[i][j+1] = 0
                elif c[i+1][j] == c[i][j+1]:
                    raise TException("c[i+1][j] == c[i][j+1]")
        
        _a[i] = dai
        _b[j] = dbj
        i += di
        j += dj
    
    return plan