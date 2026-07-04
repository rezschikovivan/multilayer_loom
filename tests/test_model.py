from unittest import TestCase, main
from loom.model.wefts import WeftsGrid, Side, Weft

class WeftTest(TestCase):
    """Класс стнлтон должен вернуть тот же экземпляр"""
    def test_instantiate_true_state(self):
        self.true_inst = Weft(True)
        self.assertAlmostEqual(self.true_inst, Weft(True))
    def test_instantiate_false_state(self):
        self.false_inst = Weft(False)
        self.assertEqual(self.false_inst, Weft(False))

class WeftsGridTest(TestCase):
    def setUp(self):
        # для каждого теста создает сетку 2х2 утка 
        self.wefts_grid = WeftsGrid()
    
    def test_set_inactive(self):
        self.wefts_grid.set_inactive(0,0)
        self.assertEqual(self.wefts_grid.wefts[0][0].is_active, False)

        self.wefts_grid.set_inactive(1,1)
        self.assertEqual(self.wefts_grid.wefts[1][1].is_active, False)

    def test_set_active(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.set_active(0,0)
        self.assertEqual(self.wefts_grid.wefts[0][0].is_active, True)

        self.wefts_grid.set_inactive(1,1)
        self.wefts_grid.set_active(1,1)
        self.assertEqual(self.wefts_grid.wefts[1][1].is_active, True)

    def test_reduce_top(self):
        self.wefts_grid.set_inactive(0,1)
        self.wefts_grid.reduce(Side.Top)
        # проверяем что удалил сверху
        self.assertListEqual(self.wefts_grid.wefts, [[Weft(False)],[Weft(True)]])

        #не должен удалять строки в ноль
        self.wefts_grid.reduce(Side.Top)
        self.assertListEqual(self.wefts_grid.wefts, [[Weft(False)],[Weft(True)]])

    def test_reduce_bottom(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.reduce(Side.Bottom)
        # проверяем что удалил снизу
        self.assertListEqual(self.wefts_grid.wefts, [[Weft(False)],[Weft(True)]])

        #не должен удалять строки в ноль
        self.wefts_grid.reduce(Side.Bottom)
        self.assertListEqual(self.wefts_grid.wefts, [[Weft(False)],[Weft(True)]])

    def test_reduce_left(self):
        self.wefts_grid.set_inactive(1,0)
        self.wefts_grid.reduce(Side.Left)
        # проверяем что удалил снизу
        self.assertListEqual(self.wefts_grid.wefts, [[Weft(False), Weft(True)]])

        #не должен удалять строки в ноль
        self.wefts_grid.reduce(Side.Left)
        self.assertListEqual(self.wefts_grid.wefts,  [[Weft(False), Weft(True)]])

    def test_reduce_right(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.reduce(Side.Right)
        # проверяем что удалил снизу
        self.assertListEqual(self.wefts_grid.wefts, [[Weft(False), Weft(True)]])

        #не должен удалять строки в ноль
        self.wefts_grid.reduce(Side.Left)
        self.assertListEqual(self.wefts_grid.wefts,  [[Weft(False), Weft(True)]])

    def test_increase_top(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.Top)
        self.assertListEqual(self.wefts_grid.wefts,  [[Weft(True), Weft(False), Weft(True)],[Weft(True), Weft(True), Weft(True)]])

    def test_increase_bottom(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.Bottom)
        self.assertListEqual(self.wefts_grid.wefts,  [[Weft(False), Weft(True), Weft(True)],[Weft(True), Weft(True), Weft(True)]])

    def test_increase_left(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.Left)
        self.assertListEqual(self.wefts_grid.wefts,  [[Weft(True), Weft(True)],[Weft(False), Weft(True)],[Weft(True), Weft(True)]])

    def test_increase_right(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.Right)
        self.assertListEqual(self.wefts_grid.wefts,  [[Weft(False), Weft(True)],[Weft(True), Weft(True)], [Weft(True), Weft(True)]])

if __name__ == "__main__":
    main()