from unittest import TestCase, main

from loom.controller import BottomlessStack, CommandManager


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

if __name__ == "__main__":
    main()
