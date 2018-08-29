import unittest
from board import Board
from disk import Disk
from manager import Manager

class ManagerUnitTest(unittest.TestCase):

    def test_is_valid_move_legal(self):
        board = Board(8)
        manager = Manager()
        move = (2, 4)
        color = Disk.DARK
        check = manager.is_valid_move(board, move, color)
        self.assertEqual(check, True)
        move = (0, 0)
        check = manager.is_valid_move(board, move, color)
        self.assertEqual(check, False)

    def test_get_possible_moves_legal(self):
        board = Board(8)
        manager = Manager()
        moves = manager.get_possible_moves(board, Disk.DARK)
        dark_moves = [(2, 4), (3, 5), (4, 2), (5, 3)]
        self.assertEqual(moves, dark_moves)
        moves = manager.get_possible_moves(board, Disk.LIGHT)
        ligth_moves = [(2, 3), (3, 2), (4, 5), (5, 4)]
        self.assertEqual(moves, ligth_moves)

    def test_disks_to_flip(self):
        board = Board(8)
        manager = Manager()
        moves = manager.get_possible_moves(board, Disk.DARK)
        move = moves[0]
        disks = manager.disks_to_flip(board, move, Disk.DARK)
        self.assertEqual(disks, [(3, 4)])

    