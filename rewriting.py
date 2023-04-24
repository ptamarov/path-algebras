import polynomial as poly
import quiver
from linalg import field
from typing import Tuple

# Refactor? A rewriting rule is just a polynomial with a chosen leading
# term. Since the order is chosen by the user, the leading term is deduced
# automatically.


class RewritingRule:
    """A rewriting rule is a pair (T, P) where T is a Path and P is a polynomial
    all whose paths are parallel to T."""

    def __init__(
        self,
        leading_term: quiver._Path,
        polynomial: poly.Polynomial,
    ) -> None:

        # Check that rewriting rule is consistent with chosen order. Guarantees termination.
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
        copy = polynomial._copy()

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


class RewritingSystem:
    """A rewriting system is initialized by a list of rewriting rules."""

    def __init__(self, rules: list[RewritingRule]) -> None:
        self.rules = rules


def rulesOverlap(rule1: RewritingRule, rule2: RewritingRule) -> bool:
    """Determine if the leading monomials m1 of rule1 and m2 of rule2 overlap,
    meaning that there are nontrivial monomials a and b such that m1 * b = a * m2."""

    m1 = rule1.leading_term  # x1 x2 x3 ... xm
    m2 = rule2.leading_term  # y1 y2 y3 ... yn

    # TODO: Complete.

    return True


def sPolynomial(rule1: RewritingRule, rule2: RewritingRule) -> poly.Polynomial | None:

    return None

    # TODO:
    # Given a pair of rewriting rules, one can compute a maximalOverlap
    # This maximalOverlap gives an sPolynomial.

    # TODO:
    # A rewriting system has to be linearly self reduced before initialization.

    # TODO:
    # A polynomial can be reduced fully with respect to a rewriting system.

    # TODO:
    # A rewriting system is confluent if all of its sPolynomials for all maximal
    # overlaps rewrite to zero.

    # TODO:
    # A rewriting system can be completed to a confluent one (for fin. dim. algebras)
    # by adding all non-zero normal forms of sPolynomials as new rewriting rules.
