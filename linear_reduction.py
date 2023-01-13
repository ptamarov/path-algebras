from polynomial import Polynomial
import polynomial


def _cleanZeros(ps: list[Polynomial]) -> list[Polynomial]:
    return [p for p in ps if p.support != []]


def isLinearlySelfReduced(listPolynomials: list[Polynomial]) -> bool:
    """Check that a list of polynomials is linearly self-reduced. This means
    that the arrows in the support of each p in the list is not equal to
    the leading term of any of the other polynomials. In other words, the
    polynomials are in echelon form (except possibly that they may not be
    monic)."""

    for p in listPolynomials:
        others_p = [q for q in listPolynomials if p != q]
        if p.isLinearlyReducedWithRespectTo(others_p):
            continue
        else:
            return False
    return True


def linearReduce(p: Polynomial, listPolynomials: list[Polynomial]) -> Polynomial:
    """Return a polynomial q such that p and q have the same coset
    modulo listPolynomials and which is linearly reduced with respect to it
    (no leading monomial in listPolynomials is equal to a monomial appearing
    in q.)

    Assumes that listPolynomials is linearly self-reduced."""
    assert isLinearlySelfReduced(listPolynomials)  # This check is expensive.

    for q in listPolynomials:
        p = p.linearReduceWithRespectTo(q)
    return p


def linearSelfReduce(ps: list[Polynomial]) -> list[Polynomial]:
    if len(ps) == 1:
        return [p * ~(p.LC()) for p in ps]

    else:
        maxes, rests = polynomial.filterPolynomialsMaximumLT(ps)
        pivot = maxes.pop()  # Get the one with max LT that was listed last.
        pivot = pivot * ~(pivot.LC())  # Make it monic.
        rest = _cleanZeros([g.linearReduceWithRespectTo(pivot) for g in maxes])
        qs = linearSelfReduce(rest + rests)

    pivot = linearReduce(pivot, qs)  # Reduce pivot.

    return [pivot] + qs  # Output list is ordered with respect to LM.
