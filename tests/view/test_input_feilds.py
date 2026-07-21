from tkinter import END, IntVar, StringVar, Tk
from unittest import TestCase, main

from loom.controller.command import CommandManager
from loom.view.input_fields import IntField, LetterField


class IntFieldTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Tk()
        cls.var = IntVar()
        cls.commander = CommandManager()
        cls.Field = IntField(cls.root, "TestIntEntry", cls.var, cls.commander)
        cls.Field.widget.focus_set()

    @classmethod
    def tearDownClass(cls):
        if cls.root:
            cls.root.destroy()

    def setUp(self):
        self.Field.widget.delete(0, END)
        self.root.update()

    def test_intfield_validation(self):
        # try invalid input
        self.Field.widget.insert(0, "ABC")
        self.Field.take_input()
        self.assertNotEqual(self.var.get(), "ABC")

        # valid input
        self.Field.widget.delete(0, END)
        self.Field.widget.insert(0, "112")
        self.Field.take_input()
        self.assertEqual(self.var.get(), 112)

    def test_intfield_reverse(self):
        self.Field.widget.insert(0, "111")
        self.Field.take_input()
        self.assertEqual(self.var.get(), 111)

        self.Field.widget.delete(0, END)
        self.root.update()
        self.Field.widget.insert(0, "222")
        self.Field.take_input()
        self.assertEqual(self.var.get(), 222)

        self.commander.undo(None)
        self.assertEqual(self.var.get(), 111)
        self.commander.redo(None)
        self.assertEqual(self.var.get(), 222)


class LetterFieldTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Tk()
        cls.var = StringVar()
        cls.commander = CommandManager()
        cls.Field = LetterField(cls.root, "TestStrEntry", cls.var, cls.commander)

    @classmethod
    def tearDownClass(cls):
        if cls.root:
            cls.root.destroy()

    def setUp(self):
        self.Field.widget.delete(0, END)

    def test_letterfield_validation(self):
        # valid input
        self.Field.widget.insert(0, "ABC")
        self.Field.take_input()
        self.assertEqual(self.var.get(), "ABC")

        # try invalid input
        self.Field.widget.delete(0, END)
        self.Field.widget.insert(0, "112")
        self.Field.take_input()
        self.assertNotEqual(self.var.get(), "ABC")

    def test_letterfield_reverse(self):
        self.Field.widget.insert(0, "A")
        self.Field.take_input()
        self.assertEqual(self.var.get(), "A")

        self.Field.widget.delete(0, END)
        self.root.update()
        self.Field.widget.insert(0, "B")
        self.Field.take_input()
        self.assertEqual(self.var.get(), "B")

        self.Field.widget.focus_set()
        self.commander.undo(None)
        self.assertEqual(self.var.get(), "A")
        self.Field.widget.focus_set()
        self.commander.redo(None)
        self.assertEqual(self.var.get(), "B")


if __name__ == "__main__":
    main()
