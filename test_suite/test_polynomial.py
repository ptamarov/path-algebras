import unittest
import quiver
import polynomial
from linalg.Q import Rational


class TestPolynomials(unittest.TestCase):
    # Q is the following quiver.
    # Path algebra is infinite dimensional.
    #      0 <────2──────╮
    #      ╰──────1────> 1 <─╮
    #                    ╰─0─╯

    def setUp(self):
        self.quiver = quiver.Quiver(
            q0=[0, 1],
            q1=[3, 1, 2],
            s={3: 1, 1: 0, 2: 1},
            t={3: 1, 1: 1, 2: 0},
        )

    def test_zero_addition(self):
        path1 = quiver._Path(0, [1, 2, 1, 2], 0, self.quiver)
        poly1 = polynomial.Polynomial([(path1, Rational(1)), (path1, Rational(-1))])
        self.assertEqual(poly1.support, [])

    def test_preprocess_same_path(self):
        path1 = quiver._Path(0, [1, 2, 1, 2], 0, self.quiver)
        poly1 = polynomial.Polynomial(
            [(path1, Rational(1, 7)), (path1, Rational(-1, 23))]
        )
        self.assertEqual(poly1.support, [path1])

    def test_addition_different_paths(self):
        path1 = quiver._Path(0, [1, 2, 1, 2], 0, self.quiver)
        path2 = quiver._Path(0, [1, 2], 0, self.quiver)
        poly1 = polynomial.Polynomial(
            [(path1, Rational(1, 7)), (path2, Rational(-1, 23))]
        )
        self.assertEqual(poly1.support, [path1, path2])

    def test_unit(self):
        idempotents = self.quiver.arrowIdeal(0, top=True)
        arrows = self.quiver.arrowIdeal(4, top=True)
        unit = polynomial.Polynomial(
            [(path, Rational(1)) for path in idempotents]
        )  # The unit of kQ is the sum of all idempotents.
        poly2 = polynomial.Polynomial([(path, Rational(1)) for path in arrows])
        self.assertEqual(poly2, unit * poly2)

    def test_idempotents(self):
        idempotents = [
            polynomial.Polynomial([(arrow, Rational(1))])
            for arrow in self.quiver.arrowIdeal(0)
        ]

        for e in idempotents:
            self.assertEqual(e, e * e)

    def test_leading_coefficient(self):
        p1 = self.quiver.createPath(0, [1, 2, 1, 2], 0)
        p2 = self.quiver.createPath(0, [1, 2], 0)
        poly1 = polynomial.Polynomial([(p1, Rational(1, 7)), (p2, Rational(-1, 23))])
        self.assertEqual(poly1.LC(), Rational(1, 7))

        q1 = self.quiver.createPath(0, [1, 2, 1, 2], 0)
        q2 = self.quiver.createPath(0, [1, 3, 3, 2], 0)
        poly2 = polynomial.Polynomial([(q1, Rational(1, 7)), (q2, Rational(-1, 23))])
        self.assertEqual(poly2.LC(), Rational(-1, 23))

    def test_filter_max_LT(self):
        p1 = self.quiver.createPath(0, [1, 2, 1, 2], 0)
        p2 = self.quiver.createPath(0, [1, 2], 0)
        poly1 = polynomial.Polynomial([(p1, Rational(1)), (p2, Rational(1))])

        q1 = self.quiver.createPath(0, [1, 2, 1, 2], 0)
        q2 = self.quiver.createPath(0, [1, 3, 3, 2], 0)
        poly2 = polynomial.Polynomial([(q1, Rational(1, 7)), (q2, Rational(1))])

        r1 = self.quiver.createPath(0, [1, 2], 0)
        r2 = self.quiver.createPath(0, [1, 3, 3, 2], 0)
        poly3 = polynomial.Polynomial([(r1, Rational(1)), (r2, Rational(-1))])

        ps = [poly1, poly2, poly3]
        max, oth = polynomial._filterPolynomialsMaximumLT(ps)

        self.assertEqual((max, oth), ([poly2, poly3], [poly1]))
