import unittest
import rewriting
import quiver
import polynomial
from linalg.Q import Rational

TEST_QUIVER = quiver.Quiver(
    q0=[0, 1],
    q1=[3, 2, 1],  # Order is x > z > y.
    s={3: 1, 1: 0, 2: 1},
    t={3: 1, 1: 1, 2: 0},
    # Default order GradedLex
)


class TestRewriting(unittest.TestCase):
    # Q is the following quiver.
    # Path algebra is infinite dimensional.
    #      0 <────z──────╮
    #      ╰──────y────> 1 <─╮
    #                    ╰─x─╯

    def setUp(self):
        self.quiver = TEST_QUIVER
        leading_term = self.quiver.createPath(1, [3, 3], 1)
        path = self.quiver.createPath(1, [2, 1], 1)
        lower_terms = polynomial.Polynomial([(path, Rational(1))])
        self.rule = rewriting.RewritingRule(leading_term, lower_terms)
        print(self.rule)

    def test_replacing(self):
        aaa = self.quiver.createPath(1, [3, 3, 3], 1)
        cb = self.quiver.createPath(1, [2, 1], 1)
        cba = self.quiver.createPath(1, [2, 1, 3], 1)
        result = aaa._replaceBy(cb, 0, 2)  # 2 - 0 = length of divisor.
        self.assertEqual(result, cba)

    def test_reduce_once1(self):
        # Test rewriting rule x^2 -> zy on x^3 - x^2zy and zyx^2.

        to_reduce1 = polynomial.Polynomial(
            [
                (self.quiver.createPath(1, [3, 3, 3], 1), Rational(1)),
                (self.quiver.createPath(1, [3, 3, 2, 1], 1), Rational(1)),
            ]
        )

        reduction1 = self.rule.reduceOnce(to_reduce1)

        expected1 = polynomial.Polynomial(
            [
                (self.quiver.createPath(1, [2, 1, 3], 1), Rational(1)),
                (self.quiver.createPath(1, [2, 1, 2, 1], 1), Rational(1)),
            ]
        )
        self.assertEqual(reduction1, expected1)

    def test_reduce_once2(self):
        to_reduce2 = polynomial.Polynomial(
            [(self.quiver.createPath(1, [2, 1, 3, 3], 1), Rational(1))]
        )
        reduction2 = self.rule.reduceOnce(to_reduce2)
        expected2 = polynomial.Polynomial(
            [
                (self.quiver.createPath(1, [2, 1, 2, 1], 1), Rational(1)),
            ]
        )
        self.assertEqual(reduction2, expected2)

    def test_reduce_fully(self):
        # Test rewriting rule a^2 -> cb on a^4 - aacbaa.
        to_reduce = polynomial.Polynomial(
            [
                (self.quiver.createPath(1, [3, 3, 3, 3], 1), Rational(1)),
                (
                    self.quiver.createPath(1, [3, 3, 2, 1, 3, 3], 1),
                    Rational(1),
                ),
            ]
        )
        expected = polynomial.Polynomial(
            [
                (self.quiver.createPath(1, [2, 1, 2, 1], 1), Rational(1)),
                (
                    self.quiver.createPath(1, [2, 1, 2, 1, 2, 1], 1),
                    Rational(1),
                ),
            ]
        )
        full_reduced = self.rule.reduceFully(to_reduce)
        self.assertEqual(full_reduced, expected)

    def test_left_divisors(self):
        path = self.quiver.createPath(1, [2, 1, 2, 1, 2, 1], 1)
        left_divisor = self.quiver.createPath(1, [2, 1, 2, 1], 1)
        not_left_divisor = self.quiver.createPath(0, [1, 2, 1, 2, 1], 1)
        vertex = self.quiver.createPath(1, [], 1)
        self.assertEqual(path._isLeftDivisibleBy(left_divisor), 3)
        self.assertEqual(path._isLeftDivisibleBy(not_left_divisor), -1)

        # Case of vertices.
        self.assertEqual(path._isLeftDivisibleBy(vertex), -1)
        vertex = self.quiver.createPath(1, [], 1)
