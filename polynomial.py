from __future__ import annotations
from quiver import _Path
import heapq
from typing import Tuple
from linalg import field
from itertools import product


class Polynomial:
    """A polynomial is a linear combination of paths with coefficients
    in a field."""

    def __init__(self, xs: list[Tuple[_Path, field.FieldScalar]]) -> None:
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

    def _copy(self) -> Polynomial:
        return Polynomial(self.polynomial[::])

    def __add__(self, other: Polynomial) -> Polynomial:
        return Polynomial(self.polynomial + other.polynomial)

    def __mul__(self, other: Polynomial | field.FieldScalar) -> Polynomial:
        """Multiplication of a polynomial by polynomials or a scalar. Returns
        a polynomial."""
        if isinstance(other, Polynomial):
            x3 = [
                (p + q, c * d)
                for (p, c), (q, d) in product(self.polynomial, other.polynomial)
                if p.target == q.source  # Guarantees * never returns NonePath.
            ]
        else:
            x3 = [(p, c * other) for (p, c) in self.polynomial]
        return Polynomial(x3)

    def __sub__(self, other: Polynomial) -> Polynomial:
        one = self.LC()._getFieldOne()
        return self + other * (-one)

    def __eq__(self, other: Polynomial) -> bool:
        return self.polynomial == other.polynomial

    def _makeMonic(self) -> Polynomial:
        """Given a non-zero polynomial f, divide it by its
        leading coefficient."""
        return self * ~(self.LC())

    def LT(self) -> Tuple[_Path, field.FieldScalar]:
        """Convenience function that returns the pair
        (path.leadingMonomial(), path.leadingCoefficient()). Raises
        ValueError if the zero polynomial is input."""

        assert self.polynomial, ValueError(
            "Zero polynomial has no leading monomial nor leading coefficient."
        )
        return self.polynomial[:][0]

    def LM(self) -> _Path:
        """Returns the largest monomial in the support of the polynomial. Raises
        ValueError if the zero polynomial is input."""

        assert self.polynomial, ValueError("Zero polynomial has no leading monomial.")
        return self.polynomial[:][0][0]

    def LC(self) -> field.FieldScalar:
        """Return the leading coefficient of a non-zero polynomial. Raises
        ValueError if the zero polynomial is input."""

        assert self.polynomial, ValueError(
            "Zero polynomial has no leading coefficient."
        )
        return self.polynomial[:][0][1]

    def _linearReduceWithRespectTo(self, q: Polynomial) -> Polynomial:
        """If LM(q) appears in the polynomial p with coefficient c, return
        p - c / LC(q) q."""
        lm, lc = q.LT()
        xs = [(m, c) for m, c in self.polynomial if m == lm]

        if xs:
            assert len(xs) == 1
            coeff = xs[0][1]
            return self - q * (coeff / lc)
        else:
            return self

    def _isLinearlyReducedWithRespectTo(self: Polynomial, ps: list[Polynomial]) -> bool:
        """Check that a polynomial is linearly reduced with respect to a list of
        polynomials. This means that no paths in the support of self is equal to
        the leading term of any of the q in ps."""
        support = self.support

        for q in ps:
            lm = q.LM()
            for path in support:
                if path == lm:
                    return False
        return True


def _pathToMonomial(path: _Path, scalar: field.FieldScalar) -> Polynomial:
    """Convert a path and a scalar into the polynomial scalar * path."""
    return Polynomial([(path, scalar)])


def _filterPolynomialsMaximumLT(
    ps: list[Polynomial],
) -> Tuple[list[Polynomial], list[Polynomial]]:
    """Returns a pair M, O where M is the list of polynomials
    with maximal leading term and O are the other (remaining) polynomials."""

    max_LT = min([p.LM() for p in ps])  # NOTE: recall order is reversed.
    maximizers, others = [], []
    for p in ps:
        if p.LM() == max_LT:
            maximizers.append(p)
        else:
            others.append(p)
    return maximizers, others


def _preProcess(
    xs: list[Tuple[_Path, field.FieldScalar]]
) -> list[Tuple[_Path, field.FieldScalar]]:

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
