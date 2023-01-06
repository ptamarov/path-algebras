from __future__ import annotations
from quiver import _Path
import heapq
from typing import Tuple
import linalg.field
from itertools import product


class Polynomial:
    """A polynomial is a linear combination of paths with coefficients
    in a field."""

    def __init__(self, xs: list[Tuple[_Path, linalg.field.FieldScalar]]) -> None:
        xs = _preProcess(xs)  # Paths are a totally ordered basis of kQ.
        self.support = [path for path, _ in xs]
        self.polynomial = xs

    def __str__(self) -> str:
        copy = self.polynomial[::]
        result = ""
        if copy:
            path, coeff = heapq.heappop(copy)
            if coeff == coeff._getFieldOne():
                result = str(path)
            elif coeff == -coeff._getFieldOne():
                result = "- " + str(path)
            else:
                result += str(coeff) + " · " + str(path)
            while copy:
                path, coeff = heapq.heappop(copy)
                if coeff == coeff._getFieldOne():
                    result += " + " + str(path)
                elif coeff == -coeff._getFieldOne():
                    result += " - " + str(path)
                else:
                    result += " + " + str(coeff) + " · " + str(path)

        return result if result else "0"

    def copy(self) -> Polynomial:
        return Polynomial(self.polynomial[::])

    def __add__(self, other: Polynomial) -> Polynomial:
        return Polynomial(self.polynomial + other.polynomial)

    def __mul__(self, other: Polynomial) -> Polynomial:
        x3 = [
            (p + q, c * d)
            for (p, c), (q, d) in product(self.polynomial, other.polynomial)
            if p.target == q.source  # Guarantees * never returns NonePath.
        ]
        return Polynomial(x3)

    def __eq__(self, other: Polynomial) -> bool:
        return self.polynomial == other.polynomial


def _pathToMonomial(path: _Path, scalar: linalg.field.FieldScalar) -> Polynomial:
    """Convert a path and a scalar into the polynomial scalar * path."""
    return Polynomial([(path, scalar)])


def _preProcess(
    xs: list[Tuple[_Path, linalg.field.FieldScalar]]
) -> list[Tuple[_Path, linalg.field.FieldScalar]]:

    heapq.heapify(xs)
    ys = []
    if xs:
        current_path, current_coefficient = heapq.heappop(xs)
        while xs:
            new_path, new_coefficient = heapq.heappop(xs)
            if new_path == current_path:
                current_coefficient += new_coefficient
            else:
                if current_coefficient != current_coefficient._getFieldZero():
                    heapq.heappush(ys, (current_path, current_coefficient))
                current_coefficient = new_coefficient
                current_path = new_path
        if current_coefficient != current_coefficient._getFieldZero():
            heapq.heappush(ys, (current_path, current_coefficient))
    # Result:
    #   1. If (path, coeff) appears in ys, then coeff is non-zero.
    #   2. If (path, coeff) appears in ys, this is the unique tuple
    #      in ys with first entry equal to path.
    #   3. Heap invariant preserved.
    return ys
