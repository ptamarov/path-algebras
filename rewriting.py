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

        # Check that rewriting rule is consisten with chosen order. Guarantees termination.
        for path in polynomial.support:
            assert leading_term < path, ValueError(
                f"""Cannot create rewriting rule!
                Issue: {leading_term} < {path} in the {leading_term.quiver.order} order.
                """
            )

        self.leading_term = leading_term
        self.polynomial = polynomial
        self.order = leading_term.quiver.order

    def __str__(self) -> str:
        return str(self.leading_term) + " ---> " + str(self.polynomial)

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

                old_polynomial_list = copy.polynomial[:]
                old_polynomial_list.pop(i)
                # TODO: Maybe one can modify polynomial in place instead by allowing
                # polynomials to consist of list of lists of paths, coeff.
                new_polynomial = poly.Polynomial(new_polynomial_list)
                copy = poly.Polynomial(old_polynomial_list) + new_polynomial
        return copy

    def reduceFully(self, polynomial: poly.Polynomial) -> poly.Polynomial:
        """Rewrites a polynomial until no path in its support is divisible by
        the leading term of the rewriting rule."""
        new_poly = self.reduceOnce(polynomial)
        old_poly = polynomial

        while new_poly != old_poly:
            old_poly = new_poly
            new_poly = self.reduceOnce(old_poly)
        return new_poly
