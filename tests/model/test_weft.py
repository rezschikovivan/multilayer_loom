from unittest import TestCase

from loom.model.weft import Side, WeftsGrid


class WeftsGridTest(TestCase):
    def setUp(self):
        # для каждого теста создает сетку 2х2 утка 
        self.wefts_grid = WeftsGrid(None, min_size=2)
        self.true_weft = self.wefts_grid._weft_factory.get_instance(True, None)
        self.false_weft = self.wefts_grid._weft_factory.get_instance(False, None)
    
    def test_init_grid(self):
        self.assertEqual(self.wefts_grid._wefts, 
        [[self.true_weft, self.true_weft],
         [self.true_weft,self.true_weft]],
           str(self.wefts_grid._wefts))

    def test_can_be_reduced(self):
        self.assertRaises(ValueError, self.wefts_grid.reduce, "right", 3)
        self.assertRaises(ValueError, self.wefts_grid.reduce, "top")
        self.assertRaises(ValueError, self.wefts_grid.reduce, "bottom", 2)
        self.assertRaises(ValueError, self.wefts_grid.reduce, "left")

        self.assertEqual(self.wefts_grid.can_be_reduced("right"), False)
        self.assertEqual(self.wefts_grid.can_be_reduced("left", 2), False)
        self.assertEqual(self.wefts_grid.can_be_reduced("top"), False)
        self.assertEqual(self.wefts_grid.can_be_reduced("bottom", 3), False)

        self.wefts_grid.increase("right", 3)

        self.assertEqual(self.wefts_grid.can_be_reduced("right"), True)
        self.assertEqual(self.wefts_grid.can_be_reduced("left", 2), True)
        self.assertEqual(self.wefts_grid.can_be_reduced("top"), False)
        self.assertEqual(self.wefts_grid.can_be_reduced("bottom", 3), False)

        self.wefts_grid.increase("top", 1)

        self.assertEqual(self.wefts_grid.can_be_reduced("right"), True)
        self.assertEqual(self.wefts_grid.can_be_reduced("left", 2), True)
        self.assertEqual(self.wefts_grid.can_be_reduced("top"), True)
        self.assertEqual(self.wefts_grid.can_be_reduced("bottom", 2), False)

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
        self.wefts_grid.increase(Side.top)
        self.wefts_grid.set_inactive(1,1)
        self.wefts_grid.reduce(Side.top)
        # проверяем что удалил сверху
        self.assertListEqual(self.wefts_grid._wefts, 
        [[self.true_weft, self.true_weft],[self.false_weft, self.true_weft]])

    def test_reduce_bottom(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.bottom)
        self.wefts_grid.reduce(Side.bottom)
        # проверяем что удалил снизу
        self.assertListEqual(self.wefts_grid._wefts, 
        [[self.true_weft, self.false_weft],[self.true_weft, self.true_weft]])

    def test_reduce_left(self):
        self.wefts_grid.set_inactive(1,1)
        self.wefts_grid.increase('left')
        self.wefts_grid.reduce(Side.left)
        # проверяем что удалил слева
        self.assertListEqual(self.wefts_grid._wefts, 
        [[self.true_weft, self.true_weft],[self.false_weft, self.true_weft]])

    def test_reduce_right(self):
        self.wefts_grid.set_inactive(1,1)
        self.wefts_grid.increase('right')
        self.wefts_grid.reduce(Side.right)
        # проверяем что удалил справа
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.true_weft, self.true_weft],[self.false_weft, self.true_weft]])

    def test_increase_top(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.top)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.true_weft, self.true_weft, 
          self.false_weft],
         [self.true_weft, self.true_weft, 
          self.true_weft]])

    def test_increase_bottom(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.bottom)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.true_weft, self.false_weft, 
          self.true_weft],
         [self.true_weft, 
          self.true_weft, 
          self.true_weft]])

    def test_increase_left(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.left)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.true_weft, self.true_weft],
         [self.true_weft, self.false_weft],
         [self.true_weft, self.true_weft]])

    def test_increase_right(self):
        self.wefts_grid.set_inactive(0,0)
        self.wefts_grid.increase(Side.right)
        self.assertListEqual(self.wefts_grid._wefts,  
        [[self.true_weft, self.false_weft],
         [self.true_weft, self.true_weft], 
         [self.true_weft, self.true_weft]])

    def test_top_repeating(self):
        self.wefts_grid.increase(Side.top, 2)
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.true_weft, self.true_weft, 
          self.true_weft, self.true_weft],
         [self.true_weft, self.true_weft, 
          self.true_weft, self.true_weft]])

        self.wefts_grid.reduce(Side.top, 2)
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.true_weft, self.true_weft],
         [self.true_weft, self.true_weft]])

    def test_bottom_repeating(self):
        self.wefts_grid.increase(Side.bottom, 2)
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.true_weft, self.true_weft, 
          self.true_weft, self.true_weft],
         [self.true_weft, self.true_weft, 
          self.true_weft, self.true_weft]])

        self.wefts_grid.reduce(Side.bottom, 2)
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.true_weft, self.true_weft],
         [self.true_weft, self.true_weft]])


    def test_right_repeating(self):
        self.wefts_grid.increase(Side.right, repeat=2)
        self.assertListEqual(self.wefts_grid._wefts,
        [
            [self.true_weft, self.true_weft],
            [self.true_weft, self.true_weft],
            [self.true_weft, self.true_weft],
            [self.true_weft, self.true_weft]
        ]
        )
        self.wefts_grid.reduce(Side.right, 2)
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.true_weft, self.true_weft],
         [self.true_weft, self.true_weft]])

    def test_left_repeating(self):
        self.wefts_grid.increase(Side.left, repeat=2)
        self.assertListEqual(self.wefts_grid._wefts,
        [
            [self.true_weft, self.true_weft],
            [self.true_weft, self.true_weft],
            [self.true_weft, self.true_weft],
            [self.true_weft, self.true_weft]
        ]
        )
        self.wefts_grid.reduce(Side.left, 2)
        self.assertListEqual(self.wefts_grid._wefts,
        [[self.true_weft, self.true_weft],
         [self.true_weft, self.true_weft]])
