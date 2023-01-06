import unittest
import rewriting
import quiver
import polynomial
from linalg.Q import Rational

TEST_QUIVER = quiver.Quiver(
    q0=[0, 1],
    q1=[0, 1, 2],
    s={0: 1, 1: 0, 2: 1},
    t={0: 1, 1: 1, 2: 0},
)


class TestTermReplacing(unittest.TestCase):
    # Q is the following quiver.
    # Path algebra is infinite dimensional.
    #      0 <────2──────╮
    #      ╰──────1────> 1 <─╮
    #                    ╰─0─╯

    def setUp(self):
        self.quiver = TEST_QUIVER
        leading_term = quiver._Path(1, [0, 0], 1, self.quiver)
        lower_terms = polynomial.Polynomial(
            [(quiver._Path(1, [2, 1], 1, self.quiver), Rational(1))]
        )
        self.rule = rewriting.RewritingRule(leading_term, lower_terms)

    def test_replacing(self):
        aaa = quiver._Path(1, [0, 0, 0], 1, self.quiver)
        cb = quiver._Path(1, [2, 1], 1, self.quiver)
        cba = quiver._Path(1, [2, 1, 0], 1, self.quiver)
        result = aaa._replaceBy(cb, 0, 2)  # 2 - 0 = length of divisor!
        self.assertEqual(result, cba)

    def test_reduce_once1(self):
        # Test rewriting rule a^2 -> cb on a^3 - aacb and cbaa.

        to_reduce1 = polynomial.Polynomial(
            [
                (quiver._Path(1, [0, 0, 0], 1, self.quiver), Rational(1)),
                (quiver._Path(1, [0, 0, 2, 1], 1, self.quiver), Rational(1)),
            ]
        )

        reduction1 = self.rule.reduceOnce(to_reduce1)

        expected1 = polynomial.Polynomial(
            [
                (quiver._Path(1, [2, 1, 0], 1, self.quiver), Rational(1)),
                (quiver._Path(1, [2, 1, 2, 1], 1, self.quiver), Rational(1)),
            ]
        )
        self.assertEqual(reduction1, expected1)

    def test_reduce_once2(self):
        to_reduce2 = polynomial.Polynomial(
            [(quiver._Path(1, [2, 1, 0, 0], 1, self.quiver), Rational(1))]
        )
        reduction2 = self.rule.reduceOnce(to_reduce2)
        expected2 = polynomial.Polynomial(
            [
                (quiver._Path(1, [2, 1, 2, 1], 1, self.quiver), Rational(1)),
            ]
        )
        self.assertEqual(reduction2, expected2)

    def test_reduce_fully(self):
        # Test rewriting rule a^2 -> cb on a^4 - aacbaa.
        to_reduce = polynomial.Polynomial(
            [
                (quiver._Path(1, [0, 0, 0, 0], 1, self.quiver), Rational(1)),
                (quiver._Path(1, [0, 0, 2, 1, 0, 0], 1, self.quiver), Rational(1)),
            ]
        )
        expected = polynomial.Polynomial(
            [
                (quiver._Path(1, [2, 1, 2, 1], 1, self.quiver), Rational(1)),
                (quiver._Path(1, [2, 1, 2, 1, 2, 1], 1, self.quiver), Rational(1)),
            ]
        )
        full_reduced = self.rule.reduceFully(to_reduce)
        self.assertEqual(full_reduced, expected)
