from unittest import TestCase, main

from loom.controller.command import bottomlessStack


class bottomlessStackTest(TestCase):
    def test_botomless(self):
        bs = bottomlessStack(2)
        for i in range(25):
            bs.append(i)
        self.assertEqual(len(bs), 2)


if __name__ == "__main__":
    main()
