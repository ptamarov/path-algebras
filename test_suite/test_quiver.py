import unittest
import quiver
import specialquivers


class TestPathClass(unittest.TestCase):
    # Q is the following quiver.
    # Path algebra is infinite dimensional.
    #      0 <────2──────╮
    #      ╰──────1────> 1 <─╮
    #                    ╰─0─╯

    def setUp(self):
        self.quiver = quiver.Quiver(
            q0=[0, 1],
            q1=[0, 1, 2],
            s={0: 1, 1: 0, 2: 1},
            t={0: 1, 1: 1, 2: 0},
        )
        self.xzyz = self.quiver.createPath(1, [0, 2, 1, 2], 0)
        self.x = self.quiver.createPath(1, [0], 1)
        self.y = self.quiver.createPath(0, [1], 1)
        self.z = self.quiver.createPath(1, [2], 0)

    def test_get_item(self):
        path1 = self.xzyz

        self.assertEqual(path1[0], self.x)
        self.assertEqual(path1[1], self.z)
        self.assertEqual(path1[2], self.y)

    def test_slicing(self):
        self.assertEqual(self.xzyz[:2], self.x + self.z)
        self.assertEqual(self.xzyz[2:], self.y + self.z)

    def test_copying(self):
        self.assertEqual(self.xzyz[:], self.xzyz)
        self.assertIsNot(self.xzyz[:], self.xzyz)

    def test_arrow_composition(self):
        path1 = self.quiver.createPath(1, [0, 2, 1, 2], 0)
        path2 = self.quiver.createPath(0, [1, 0, 2, 1], 1)
        path3 = self.quiver.createPath(1, [0, 2, 1, 2, 1, 0, 2, 1], 1)
        self.assertEqual(path1 + path2, path3)

    # TODO: Check NonePath and non-composable arrows.

    def test_find(self):
        find_in = self.quiver.createPath(1, [2, 1, 0, 0], 1)
        find = self.quiver.createPath(1, [0, 0], 1)
        self.assertEqual(find_in._find(find), 2)


class TestA5(unittest.TestCase):
    def test_number_of_arrows_A5(self):
        Q = specialquivers.createDynkinA(10)
        for k in range(1, 10):
            self.assertEqual(len(Q.arrowIdeal(k, top=True)), 10 - k)
