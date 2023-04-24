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
        if p._isLinearlyReducedWithRespectTo(others_p):
            continue
        else:
            return False
    return True


def linearSelfReduce(ps: list[Polynomial]) -> list[Polynomial]:
    """Compute the linear self reduction of a list of polynomials. This
    is equivalent to computing the row reduced echelon form of the matrix
    corresponding to these polynomials with respect to the ordered basis of
    paths given by the chosen monomial order.
    """
    processed: list[Polynomial] = []

    if len(ps) == 1:
        return [p * ~(p.LC()) for p in ps]

    while len(ps) > 0:
        maxes, rests = polynomial._filterPolynomialsMaximumLT(ps)
        pivot = maxes.pop()  # Get the one with max LT that was listed last.
        processed.append(pivot * ~(pivot.LC()))  # Make it monic.
        rest = _cleanZeros([g._linearReduceWithRespectTo(pivot) for g in maxes])
        ps = rest + rests

    result = []
    counter = len(processed) - 1

    while counter >= 0:
        pivot = processed.pop()
        result.append(pivot)
        for i in range(counter):
            processed[i] = processed[i]._linearReduceWithRespectTo(pivot)
        counter -= 1
    return result[::-1]
