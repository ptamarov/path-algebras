import unittest
import linalg.linearalg as linearalg
from linalg.Q import Rational as Q
from linalg.Q import Rationals as QQ


class TestLinAlg(unittest.TestCase):
    def test_inverse(self):
        N = 3
        A = linearalg.Matrix(
            QQ(), [[Q(1, i + j + 1) for i in range(N)] for j in range(N)]
        )
        B = linearalg.Matrix(
            QQ(),
            [
                [Q(9), Q(-36), Q(30)],
                [Q(-36), Q(192), Q(-180)],
                [Q(30), Q(-180), Q(180)],
            ],
        )
        self.assertEqual(A.invert(), B)

    def test_RREF(self):
        B = linearalg.Matrix(
            QQ(),
            [
                [Q(1), Q(0), Q(1, 3), Q(0), Q(9, 5)],
                [Q(0), Q(1), Q(-1, 2), Q(0), Q(5)],
                [Q(0), Q(0), Q(0), Q(1), Q(2)],
            ],
        )  # B is already in RREF.

        self.assertEqual(B, B.RREF())
