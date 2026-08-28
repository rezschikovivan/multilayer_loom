from unittest import TestCase, main

from src.loom.controller import BottomlessStack, CommandManager, Memento, Originator


class BottomlessStackTest(TestCase):
    def test_botomless(self):
        bs = BottomlessStack(2)
        for i in range(25):
            bs.append(i)
        self.assertEqual(len(bs), 2)

class SingletonManagerTest(TestCase):
    def test_singleton_manager(self):
        mnger1 = CommandManager()
        mnger2 = CommandManager()
        self.assertTrue(mnger1 is mnger2)

class MementoTest(TestCase):
    def test_permission(self):
        class SubOriginator(Originator):
            def set_memento(self, memento):
                self.state = memento.get_state(self)

            def create_memento(self):
                return Memento(self, "Hello")
            
        orig = SubOriginator()
        mem = orig.create_memento()
        self.assertRaises(PermissionError, mem.get_state, self)
        self.assertEqual(mem.get_state(orig), "Hello")

if __name__ == "__main__":
    main()
