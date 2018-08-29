import unittest
from board import Board
from disk import Disk

class BoeardUnitTest(unittest.TestCase):

    def test_constructor_default(self):
        board = Board(8)
        pos = (0, 0)
        value = board.get_cel(pos)
        self.assertEqual(value, Disk.NONE)
        pos = (4, 4)
        value = board.get_cel(pos)
        self.assertEqual(value, Disk.DARK)
        pos = (4, 3)
        value = board.get_cel(pos)
        self.assertEqual(value, Disk.LIGHT)

    def test_constructor_with_existing_data(self):
        data = [[Disk.DARK] * 5] * 5
        board = Board(5, data)
        pos = (0, 0)
        value = board.get_cel(pos)
        self.assertEqual(value, Disk.DARK)
        pos = (4, 4)
        value = board.get_cel(pos)
        self.assertEqual(value, Disk.DARK)
        pos = (2, 3)
        value = board.get_cel(pos)
        self.assertEqual(value, Disk.DARK)

    def test_change_cel(self):
        board = Board(8)
        board.change_cel((5, 5), Disk.DARK)
        pos = (5, 5)
        value = board.get_cel(pos)
        self.assertEqual(value, Disk.DARK)