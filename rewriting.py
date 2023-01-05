import polynomial
import quiver


class RewritingRule:
    """A rewriting rule is a pair (T, P) where T is a Path and P is a polynomial
    all whose paths are parallel to T."""

    def __init__(
        self,
        leading_term: quiver._Path,
        polynomial: polynomial.Polynomial,
        order: quiver.PathOrder,
    ) -> None:
        pass
