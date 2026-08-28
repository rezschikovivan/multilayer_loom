from unittest import TestCase

from src.loom.model.model_bases import InstanceFactory
from src.loom.model.weft import Weft


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

        self.assertRaises(TypeError, self.factory.get_instance, True, "Hello", {"HI":1})
