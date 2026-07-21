from unittest import TestCase

from loom.model.weft import Side, WeftsGrid


class WeftsGridTest(TestCase):
    def setUp(self):
        # для каждого теста создает сетку 2х2 утка 
        self.wefts_grid = WeftsGrid(None)
        self.args_false = (False, None)
        self.args_true  = (True, None)
    
    def test_init_grid(self):
        self.assertEqual(self.wefts_grid._wefts, 
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true),self.wefts_grid._weft_factory.get_instance(*self.args_true)]],
           str(self.wefts_grid._wefts))

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
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true), 
          self.wefts_grid._weft_factory.get_instance(*self.args_false)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true), 
          self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

    def test_increase_bottom(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.bottom)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_false), 
          self.wefts_grid._weft_factory.get_instance(*self.args_true)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), 
          self.wefts_grid._weft_factory.get_instance(*self.args_true), 
          self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

    def test_increase_left(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.left)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_false)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

    def test_increase_right(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.right)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_false)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)], 
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

    def test_top_repeating(self):
        self.wefts_grid.increase(Side.top, 2)
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true), 
          self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true), 
          self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

        self.wefts_grid.reduce(Side.top, 2)
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

    def test_bottom_repeating(self):
        self.wefts_grid.increase(Side.bottom, 2)
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true), 
          self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true), 
          self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

        self.wefts_grid.reduce(Side.bottom, 2)
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])


    def test_right_repeating(self):
        self.wefts_grid.increase(Side.right, repeat=2)
        self.assertListEqual(self.wefts_grid._wefts,
        [
            [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
            [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
            [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
            [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]
        ]
        )
        self.wefts_grid.reduce(Side.right, 2)
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])

    def test_left_repeating(self):
        self.wefts_grid.increase(Side.left, repeat=2)
        self.assertListEqual(self.wefts_grid._wefts,
        [
            [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
            [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
            [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
            [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]
        ]
        )
        self.wefts_grid.reduce(Side.left, 2)
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)],
         [self.wefts_grid._weft_factory.get_instance(*self.args_true), self.wefts_grid._weft_factory.get_instance(*self.args_true)]])
