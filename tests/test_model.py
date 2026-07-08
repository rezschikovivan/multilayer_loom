from unittest import TestCase, main

from loom.model.wefts import Side, Weft, WeftsGrid, InstanceFactory, Warp

class TestInstanceFactory(TestCase):
    def setUp(self):
        self.factory = InstanceFactory(Weft)
        self.args_1 = (False, 1)
        self.args_2 = (True, 1)

    def test_get_instance(self):
        inst_1 = self.factory.get_instance(*self.args_2)
        inst_2 = self.factory.get_instance(*self.args_2)
        self.assertEqual(inst_1, inst_2)

        inst_3 = self.factory.get_instance(*self.args_1)
        self.assertNotEqual(inst_2, inst_3)

        inst_4 = self.factory.get_instance(*self.args_1)
        self.assertEqual(inst_3, inst_4)

        try:
            inst_5 = self.factory.get_instance(True, "Hello", {"HI":1})
        except BaseException as err:
            self.assertIsInstance(err, KeyError)
        else:
            raise RuntimeError(f"Фабрика успешно приняла невалидные данные и вернула: {inst_5}, вместо исключения!")


class WeftsGridTest(TestCase):
    def setUp(self):
        # для каждого теста создает сетку 2х2 утка 
        self.wefts_grid = WeftsGrid(None)
        self.args_false = (False, None)
        self.args_true = (True, None)
    
    def test_set_inactive(self):
        self.wefts_grid.set_inactive(0,0)
        self.assertEqual(self.wefts_grid.get_weft(0,0).is_active, False)

        self.wefts_grid.set_inactive(1,1)
        self.assertEqual(self.wefts_grid.get_weft(1,1).is_active, False)

    def test_set_active(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.set_active(0,0)
        self.assertEqual(self.wefts_grid.get_weft(0,0).is_active, True)

        self.wefts_grid.set_inactive(1,1)
        self.wefts_grid.set_active(1,1)
        self.assertEqual(self.wefts_grid.get_weft(1,1).is_active, True)

    def test_reduce_top(self):
        self.wefts_grid.set_inactive(0,1)
        self.wefts_grid.reduce(Side.top)
        # проверяем что удалил сверху
        self.assertListEqual(self.wefts_grid._wefts, 
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true)],[self.wefts_grid._weft_factory.get_instance(*self.args_false)]])

        #не должен удалять строки в ноль
        self.wefts_grid.reduce(Side.top)
        self.assertListEqual(self.wefts_grid._wefts, 
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true)],[self.wefts_grid._weft_factory.get_instance(*self.args_false)]])

    def test_reduce_bottom(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.reduce(Side.bottom)
        # проверяем что удалил снизу
        self.assertListEqual(self.wefts_grid._wefts, 
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true)],[self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

        #не должен удалять строки в ноль
        self.wefts_grid.reduce(Side.bottom)
        self.assertListEqual(self.wefts_grid._wefts, 
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true)],[self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

    def test_reduce_left(self):
        self.wefts_grid.set_inactive(1,0)
        self.wefts_grid.reduce(Side.left)
        # проверяем что удалил снизу
        self.assertListEqual(self.wefts_grid._wefts, 
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

        #не должен удалять строки в ноль
        self.wefts_grid.reduce(Side.left)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

    def test_reduce_right(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.reduce(Side.right)
        # проверяем что удалил снизу
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_false)]])

        #не должен удалять строки в ноль
        self.wefts_grid.reduce(Side.left)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_false)]])

    def test_increase_top(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.top)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_false)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

    def test_increase_bottom(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.bottom)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_false), self.wefts_grid._weft_factory.get_instance(*self.args_true)],[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

    def test_increase_left(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.left)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_false)],[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

    def test_increase_right(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.right)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_false)],[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)], [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

class TestWarp(TestCase):
    def setUp(self):
        self.warp = Warp(1)
if __name__ == "__main__":
    main()