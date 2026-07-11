from unittest import TestCase, main

from loom.model.weft import Side, Weft, InstanceFactory
from loom.model.warp import Warp

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




class TestWarp(TestCase):
    def setUp(self):
        self.warp = Warp(None, 5)

    def test_init(self):
        self.assertEqual(self.warp.length, 5)
        self.assertEqual(self.warp.get_points(0), 
                         [[0,0],[1,0],[2,0],[3,0],[4,0]])

    def test_seting_anchor(self):
        self.warp.set_anchor(0,)

    def test_add_length(self):
        self.warp._add_length(1, Side.right)
        self.assertEqual(self.warp.length, 6)

    def test_remove_lenth(self):
        self.warp._remove_length(2)
        self.assertEqual(self.warp.length, 3)

if __name__ == "__main__":
    main()