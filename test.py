from cli import CLI
from disk import Disk
from board import Board
from manager import Manager
from human_player import HumanPlayer

console = CLI()
man = Manager()
board = Board(8)

console.display_board(board)

moves = man.get_possible_moves(board, Disk.LIGHT)

print(moves)

move = moves[0]

disks = man.disks_to_flip(board, move, Disk.LIGHT)

print(disks)

console.display_board(board)

print("\n\n\n")
man.play_move(board, move, Disk.LIGHT)

console.display_board(board)

print("\n\n\n")
man.play_move(board, (2, 2), Disk.DARK)

console.display_board(board)

p1 = HumanPlayer(Disk.DARK)

move = p1.get_move(board, moves, console)

print(move)

