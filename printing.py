ALPHA = True  # Must be later controlled by user.
GREEK_SYMBS = [chr(c) for c in range(0x3B1, 0x3E2)]
GREEK_DICT = {i: c for i, c in enumerate(GREEK_SYMBS) if c.isalpha()}
SUPS = {0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹"}
SUBS = {0: "₀", 1: "₁", 2: "₂", 3: "₃", 4: "₄", 5: "₅", 6: "₆", 7: "₇", 8: "₈", 9: "₉"}


def _toSup(n: int) -> str:
    if n == 1:
        return ""
    else:
        return "".join([SUPS[int(i)] for i in list(str(n))])


def _toSub(n: int) -> str:
    return "".join([SUBS[int(i)] for i in list(str(n))])


def _toVar(n: int):
    return GREEK_DICT[n] if not ALPHA else (GREEK_SYMBS[0] + _toSub(n))
