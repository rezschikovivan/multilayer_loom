from unittest import TestCase

from loom.model.warp import Side, Warp, WarpsLines
from loom.model.weft import WeftsGrid


class TestWarp(TestCase):
    def setUp(self):
        self.warp = Warp(None, 5)

    def test_init_and_get_points(self):
        """Проверка корректности инициализации класса"""
        self.assertEqual(self.warp.length, 5)
        self.assertEqual(self.warp.get_points(0), 
                         [[0,0],[1,0],[2,0],[3,0],[4,0]])

    def test_seting_anchor(self):
        """Проверка установки точек"""
        self.warp.set_anchor(0, 0, 2)
        self.assertEqual(self.warp.get_points(), [[0,2],[1,0],[2,0],[3,0],[4,0]])

    def test_add_length(self):
        """Проверка добавления длинны"""
        #добавляем 1 справа
        self.warp.set_anchor(0, self.warp.length-1, 8)
        self.warp._add_length(6, Side.right)
        self.assertListEqual(self.warp.get_points(), [[0,0],[1,0],[2,0],[3,0],[4,8],[5,0]])
        # добавляем 2 слева
        self.warp.set_anchor(0, 0, 9)
        self.warp._add_length(8, Side.left)
        self.assertListEqual(self.warp.get_points(), [[0,0],[1,0],[2,9],[3,0],[4,0],[5,0],[6,8],[7,0]])
        # методом добавления нельзя уменьшить длинну
        self.assertRaises(ValueError, self.warp._add_length, 6, Side.right)
        self.assertRaises(ValueError, self.warp._add_length, 2, Side.left)

    def test_remove_length(self):
        """Проверка уменьшения длинны"""
        #проверяем уменьшение на 1
        self.warp.set_anchor(0, 0, 2)
        self.warp._remove_length(4, Side.right)
        self.assertEqual(self.warp.get_points(), [[0,2],[1,0],[2,0],[3,0]])
        #проверяем уменьшение на 2 (>1)
        self.warp.set_anchor(0, 2, 5)
        self.warp._remove_length(2, Side.left)
        self.assertEqual(self.warp.get_points(), [[0,5],[1,0]])
        # методом уменьшения нельзя добавить длинну
        self.assertRaises(ValueError, self.warp._remove_length, 6, Side.right)
        self.assertRaises(ValueError, self.warp._remove_length, 6, Side.left)
        
    def test_update_warp_right(self):
        """Проверка обновления длинны справа"""
        self.warp.set_anchor(0, 0, 7)
        wefts_grid = WeftsGrid(None, 10, 5)
        self.warp.update(0, wefts_grid, Side.right)
        self.assertEqual(self.warp.length, 10) # проверяем обновилась ли длинна
        # проверяем корректность обновления точек точек
        self.assertNotEqual(self.warp.get_points(), [[0,7],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0]])
        self.assertEqual(self.warp.get_points(),    [[0,5],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0]])

    def test_update_warp_left(self):
        """Проверка обновления длинны слева"""
        self.warp.set_anchor(0, 0, 8)
        wefts_grid = WeftsGrid(None, 10, 5)
        self.warp.update(0, wefts_grid, Side.left)
        self.assertEqual(self.warp.length, 10) # проверяем обновилась ли длинна
        # проверяем корректность обновления точек точек
        self.assertNotEqual(self.warp.get_points(), [[0,0],[1,0],[2,0],[3,0],[4,0],[5,8],[6,0],[7,0],[8,0],[9,0]])
        self.assertEqual(self.warp.get_points(),    [[0,0],[1,0],[2,0],[3,0],[4,0],[5,5],[6,0],[7,0],[8,0],[9,0]])

    def test_update_warp_height(self):
        """Проверка обновления точек после изменения индекса утка"""
        self.warp.set_anchor(0, 0, 8)
        wefts_grid = WeftsGrid(None, 10, 5)
        self.warp.update(0, wefts_grid, Side.left)
        self.assertEqual(self.warp.get_points(), [[0,0],[1,0],[2,0],[3,0],[4,0],[5,5],[6,0],[7,0],[8,0],[9,0]])
        self.warp.update(1, wefts_grid, Side.left)
        self.assertEqual(self.warp.get_points(), [[0,0],[1,0],[2,0],[3,0],[4,0],[5,4],[6,0],[7,0],[8,0],[9,0]])
        self.warp.update(3, wefts_grid, Side.left)
        self.assertEqual(self.warp.get_points(), [[0,0],[1,0],[2,0],[3,0],[4,0],[5,2],[6,0],[7,0],[8,0],[9,0]])

class TestWarpLines(TestCase):
    def setUp(self):
        self.wefts_grid = WeftsGrid(None, 2, 2)
        self.lines = WarpsLines(None, self.wefts_grid)
    
    def test_init(self):
        """
        Проверка корректности инициализациии списка основы
        должно быть на 1 больше чем высота сетки утков.
        """
        self.assertEqual(self.lines.warps.__len__(), 3)

    def test_get(self):
        self.assertEqual(self.lines.warps[0], self.lines.get_warp(0))

    def test_set_warp_anchor(self):
        """Проверак установки точек привязки основы"""
        index = 0
        self.lines.set_warp_anchor(index,0,1)
        self.assertEqual(self.lines.warps[index].anchor_points, [1,0])

        self.lines.set_warp_anchor(index,0,100)
        self.assertEqual(self.lines.warps[index].anchor_points, [2,0])

        index = 1 #  берем другую основу и проверяем корректность установки
        self.lines.set_warp_anchor(index,1,2)
        self.assertEqual(self.lines.warps[index].anchor_points, [0,1])

        #установка отрицатиельного якоря относительно индекса основы
        index = 2
        self.lines.set_warp_anchor(index,0,0)
        self.assertEqual(self.lines.warps[index].anchor_points, [-2,0])
        
        #попытка ввода отрицательных точек
        self.assertRaises(ValueError, self.lines.set_warp_anchor, 0,-4,0)
        self.assertRaises(ValueError, self.lines.set_warp_anchor, 0,0,-5)
        self.assertRaises(ValueError, self.lines.set_warp_anchor, 0,-6,-8)

        #попытка ввода точки с положительой несуществующей колонкой (х)
        self.assertRaises(ValueError, self.lines.set_warp_anchor, 0,9,0)

    def test_increase(self):
        """Проверка добавления основ"""
        # нельзя добавить основы справа или слева, только сверху или снизу
        self.assertRaises(ValueError, self.lines.increase, Side.right)
        self.assertRaises(ValueError, self.lines.increase, Side.left)

        # добавление сверху
        warp_indx = 1
        self.lines.set_warp_anchor(warp_indx,1,2)
        self.lines.increase(Side.top)
        self.assertEqual(self.lines.warps.__len__(), 4) # длина изменилась
        # точка не сдинулась т.к. добавили сверху
        self.assertListEqual(self.lines.warps[warp_indx].anchor_points, [0,1])

        # добавление снизу несколько раз
        warp_indx = 0
        self.lines.set_warp_anchor(warp_indx,1,2)
        self.lines.increase(Side.bottom, 2)
        self.assertEqual(self.lines.lines_count, 6) # длина изменилась
        # точка сдинулась т.к. добавили снизу
        self.assertListEqual(self.lines.warps[warp_indx].anchor_points, [0,0])

    def test_reduce(self):
        """Проверка удаления основ"""
        # нельзя удалить основы справа или слева, только сверху или снизу
        self.assertRaises(ValueError, self.lines.reduce, Side.right)
        self.assertRaises(ValueError, self.lines.reduce, Side.left)
        # удаление сверху
        index = 0
        self.lines.set_warp_anchor(index,1,1)
        self.lines.reduce(Side.top)
        self.assertEqual(self.lines.lines_count, 2)
        self.assertListEqual(self.lines.warps[index].anchor_points, [0,1])

        self.setUp()
        # удаление снизу несколько раз
        index = 2
        self.lines.set_warp_anchor(index, 0, 1)
        self.lines.reduce(Side.bottom, 2)
        self.assertEqual(self.lines.lines_count, 1)
        self.assertListEqual(self.lines.warps[0].anchor_points, [-1,0])
        # удаления элементов в 0 не должно быть
        self.lines.reduce(Side.bottom)
        self.assertEqual(self.lines.lines_count, 1)
        self.lines.reduce(Side.top)
        self.assertEqual(self.lines.lines_count, 1)

    def test_update(self):
        """Проверка обновления количества основ при изменении сетки утков"""
        #increase
        self.assertEqual(self.lines.lines_count, 3)
        self.wefts_grid.increase(Side.top)
        self.assertEqual(self.lines.lines_count, 4)
        self.wefts_grid.increase(Side.bottom, 2)
        self.assertEqual(self.lines.lines_count, 6)
        #reduce
        self.wefts_grid.reduce(Side.top, 2)
        self.assertEqual(self.lines.lines_count, 4)
        self.wefts_grid.reduce(Side.bottom, 2)
        self.assertEqual(self.lines.lines_count, 2)

    def test_update_warps_by_wefts_grid(self):
        """Проверка измененя точек привязки основ при изменении сетки утков"""
        # при удалении сверху
        self.lines.set_warp_anchor(0, 1, 2)
        self.assertListEqual(self.lines.warps[0].anchor_points, [0,2])
        self.wefts_grid.reduce(Side.top)
        self.assertListEqual(self.lines.warps[0].anchor_points, [0,1])

        self.setUp()
        self.wefts_grid.increase(Side.top, 2)# при добавлении никаких доп действий не предусмотрено
        self.lines.set_warp_anchor(4, 0, 0)
        self.assertListEqual(self.lines.warps[4].anchor_points, [-4,0])
        self.wefts_grid.reduce(Side.bottom, 3)
        self.assertListEqual(self.lines.warps[self.lines.lines_count-1].anchor_points, [-1,0])

        #