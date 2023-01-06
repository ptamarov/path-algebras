import heapq
import polynomial as poly
import quiver
from linalg import field
from typing import Tuple


class RewritingRule:
    """A rewriting rule is a pair (T, P) where T is a Path and P is a polynomial
    all whose paths are parallel to T."""

    def __init__(
        self,
        leading_term: quiver._Path,
        polynomial: poly.Polynomial,
    ) -> None:

        self.leading_term = leading_term
        self.polynomial = polynomial
        self.order = leading_term.order
        # TODO: Check that rewriting rule is consistent with order.

    def reduceOnce(self, polynomial: poly.Polynomial) -> poly.Polynomial:
        """Reduce all arrows that are divisible by the leading term of
        the rewriting rule once. Reduces the first occurrence of a divisor
        only."""
        copy = polynomial.copy()

        for i in range(len(copy.polynomial)):
            term, scalar = copy.polynomial[i]
            start = term._find(self.leading_term)
            if start != -1:
                new_polynomial_list: list[Tuple[quiver._Path, field.FieldScalar]] = []
                for arrow, coefficient in self.polynomial.polynomial:
                    new_term = (
                        term._replaceBy(arrow, start, len(self.leading_term)),
                        scalar * coefficient,
                    )
                    new_polynomial_list += [new_term]

                old_polynomial_list = copy.polynomial[::]
                old_polynomial_list.pop(i)
                # TODO: Maybe one can modify polynomial in place instead by allowing
                # polynomials to consist of list of lists of paths, coeff.
                new_polynomial = poly.Polynomial(new_polynomial_list)
                copy = poly.Polynomial(old_polynomial_list) + new_polynomial
        return copy

    def reduceFully(self, polynomial: poly.Polynomial) -> poly.Polynomial:
        new_poly = self.reduceOnce(polynomial)
        old_poly = polynomial

        while new_poly != old_poly:
            old_poly = new_poly
            new_poly = self.reduceOnce(old_poly)
        return new_poly
