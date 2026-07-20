from unittest import TestCase, main

from loom.controller.command import BottomlessStack


class BottomlessStackTest(TestCase):
    def test_botomless(self):
        bs = BottomlessStack(2)
        for i in range(25):
            bs.append(i)
        self.assertEqual(len(bs), 2)


if __name__ == "__main__":
    main()
