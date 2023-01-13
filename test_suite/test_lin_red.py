import unittest
import quiver
from polynomial import Polynomial
from linalg.Q import Rational
import linear_reduction

TEST_QUIVER = quiver.Quiver(q0=[0], q1=[1], s={1: 0}, t={1: 0})

# Helper.
def X(n: int):
    return Polynomial(
        [(TEST_QUIVER.createPath(0, [1 for _ in range(n)], 0), Rational(1))]
    )


class TestLinearReduction(unittest.TestCase):
    # Q is the following quiver. Path algebra is k[x] (polynomials in one variable).
    #  0 <─╮
    #  ╰─x─╯

    def setUp(self):
        self.quiver = TEST_QUIVER

    def test_single_linear_reduction(self):
        pol1 = X(5) + X(4) * Rational(3) + X(2) * Rational(2)
        pol2 = X(4) * Rational(2) + X(3) * Rational(1) + X(2) * Rational(1)
        pol3 = pol1 - pol2 * Rational(3, 2)

        self.assertEqual(pol1._linearReduceWithRespectTo(pol2), pol3)

    def test_linear_self_reduction(self):
        pol1 = X(5) + X(4) * Rational(3) + X(2) * Rational(2)
        pol2 = X(4) * Rational(2) + X(3) + X(2)
        pol3 = X(4) + X(3) * Rational(-6) + X(1) * Rational(-3)
        xs = [pol1, pol2, pol3]

        # Matrix w.r.t usual order is:
        # 1  3  2  0  0
        # 0  2  1  1  0
        # 0  1 -6  0 -3

        # RREF is:
        # 1  0  0   8/13   9/13
        # 0  1  0   6/13  -3/13
        # 0  0  1   1/13   6/13

        ys = linear_reduction.linearSelfReduce(xs)
        new1 = X(5) + X(2) * Rational(8, 13) + X(1) * Rational(9, 13)
        new2 = X(4) + X(2) * Rational(6, 13) + X(1) * Rational(-3, 13)
        new3 = X(3) + X(2) * Rational(1, 13) + X(1) * Rational(6, 13)

        self.assertEqual(ys, [new1, new2, new3])
