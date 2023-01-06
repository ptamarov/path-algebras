import unittest
import quiver
import specialquivers


class TestIncomingArrows(unittest.TestCase):
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

    def test_arrow_composition(self):
        factory = quiver.PathFactory(quiver.DegLex())
        path1 = factory.createPath(1, [0, 2, 1, 2], 0, self.quiver)
        path2 = factory.createPath(0, [1, 0, 2, 1], 1, self.quiver)
        path3 = factory.createPath(1, [0, 2, 1, 2, 1, 0, 2, 1], 1, self.quiver)
        self.assertEqual(path1 + path2, path3)

    # TODO: Check NonePath and non-composable arrows.

    def test_find(self):
        find_in = quiver._Path(1, [2, 1, 0, 0], 1, self.quiver)
        find = quiver._Path(1, [0, 0], 1, self.quiver)
        self.assertEqual(find_in._find(find), 2)


class TestA5(unittest.TestCase):
    def test_number_of_arrows_A5(self):
        Q = specialquivers.createDynkinA(10)
        for k in range(1, 10):
            self.assertEqual(len(Q.arrowIdeal(k, top=True)), 10 - k)
