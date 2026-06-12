from unittest import TestCase, main
from tkinter import Tk, IntVar, StringVar, END

from loom.controller.input_feilds import IntFeild, LetterFeild, Command

class IntFeildTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Tk()
        cls.var = IntVar()
        cls.feild = IntFeild(cls.root, "TestIntEntry", cls.var)
        cls.root.bind_all("<Control-z>", Command.manager.unexecute)
        cls.root.bind_all("<Control-y>", Command.manager.reverse_unexecute)
        cls.feild.widget.focus_set()
    @classmethod
    def tearDownClass(cls):
        if cls.root:
            cls.root.destroy()
        
    def setUp(self):
        self.feild.widget.delete(0, END)

    def test_intfeild_validation(self):
        # try invalid input
        self.feild.widget.insert(0,"ABC")
        self.root.update()
        self.feild.widget.event_generate("<Key-Return>")
        self.root.update()
        self.assertNotEqual(self.var.get(), "ABC")

        # valid input
        self.feild.widget.delete(0, END)
        self.feild.widget.insert(0,"112")
        self.root.update()
        self.feild.widget.event_generate("<Key-Return>")
        self.root.update()
        self.assertEqual(self.var.get(), 112)

    def test_intfeild_reverse(self):
        self.feild.widget.insert(0,"111")
        self.root.update()
        self.feild.widget.event_generate("<Key-Return>")
        self.root.update()
        self.assertEqual(self.var.get(), 111)

        self.feild.widget.delete(0, END)
        self.root.update()
        self.feild.widget.insert(0, "222")
        self.root.update()
        self.feild.widget.event_generate("<Key-Return>")
        self.root.update()
        self.assertEqual(self.var.get(), 222)

        self.feild.widget.event_generate("<Control-z>")
        self.assertEqual(self.var.get(), 111)
        self.feild.widget.event_generate("<Control-y>")
        self.assertEqual(self.var.get(), 222)

class LetterFeildTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Tk()
        cls.var = StringVar()
        cls.feild = LetterFeild(cls.root, "TestStringEntry", cls.var)
        cls.root.bind_all("<Control-z>", Command.manager.unexecute)
        cls.root.bind_all("<Control-y>", Command.manager.reverse_unexecute)
        cls.feild.widget.focus_set()
    @classmethod
    def tearDownClass(cls):
        if cls.root:
            cls.root.destroy()
        
    def setUp(self):
        self.feild.widget.delete(0, END)

    def test_intfeild_validation(self):
        # valid input
        self.feild.widget.insert(0,"ABC")
        self.root.update()
        self.feild.widget.event_generate("<Key-Return>")
        self.root.update()
        self.assertEqual(self.var.get(), "ABC")

        # try invalid input
        self.feild.widget.delete(0, END)
        self.feild.widget.insert(0,"112")
        self.root.update()
        self.feild.widget.event_generate("<Key-Return>")
        self.root.update()
        self.assertNotEqual(self.var.get(), 112)

    def test_intfeild_reverse(self):
        self.feild.widget.insert(0,"A")
        self.root.update()
        self.feild.widget.event_generate("<Key-Return>")
        self.root.update()
        self.assertEqual(self.var.get(), "A")

        self.feild.widget.delete(0, END)
        self.root.update()
        self.feild.widget.insert(0, "B")
        self.root.update()
        self.feild.widget.event_generate("<Key-Return>")
        self.root.update()
        self.assertEqual(self.var.get(), "B")

        self.feild.widget.event_generate("<Control-z>")
        self.assertEqual(self.var.get(), "A")
        self.feild.widget.event_generate("<Control-y>")
        self.assertEqual(self.var.get(), "B")

if __name__ == "__main__":
    main()