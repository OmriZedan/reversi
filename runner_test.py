from cli import CLI
from disk import Disk
from board import Board
from manager import Manager
from human_player import HumanPlayer
from random_player import RandomPlayer
from simple_player import SimplePlayer
from minimax_player import Player02
from runner import Runner

game = Runner(board_size=8, player1_type=Player02, player2_type=RandomPlayer)
p1_wins, p2_wins = 0, 0

for i in range(1, 20):
    print(f"Game {i} started")
    game = Runner(board_size=8, player1_type=Player02, player2_type=RandomPlayer)
    winner = game.run_game()
    if winner == Disk.DARK:
        p1_wins += 1
    elif winner == Disk.LIGHT:
        p2_wins += 1


print(f"X won {p1_wins} Times")
print(f"O won {p2_wins} Times")