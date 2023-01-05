# Masks for simple functions to use dictionaries like "set functions".


def eval(f: dict[int, int], z: int) -> int:
    assert z in f.keys(), ValueError("Input is not in the domain of function.")
    return f[z]


def codomain(f: dict[int, int]) -> set:
    return set(f.values())


def domain(f: dict[int, int]) -> set:
    return set(f.keys())


def preimage(f: dict[int, int], x: int) -> list:
    return [u for u in domain(f) if f[u] == x]
