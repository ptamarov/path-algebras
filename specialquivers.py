from quiver import Quiver


def createDynkinA(n: int) -> Quiver:
    """Create the Dyniking quiver of type A with n vertices
    and all vertices combed in one direction."""

    q0 = [i for i in range(n)]
    q1 = [i for i in range(n - 1)]
    s = {i: i for i in range(n - 1)}
    t = {i: i + 1 for i in range(n - 1)}

    return Quiver(q0, q1, s, t, name=f"A{n}")


def createDynkinD(n: int) -> Quiver:
    """Create the Dyniking quiver of type D with n vertices
    and all vertices combed in the direction of the unique
    vertex of degree 3."""

    q0 = [i for i in range(n + 1)]
    q1 = [i + 1 for i in range(n)]
    s = {i: i - 1 for i in range(1, n)} | {n: n - 1}
    t = {i: i + 1 for i in range(1, n - 1)} | {n: n}

    return Quiver(q0, q1, s, t, name=f"D{n}")
