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

game.run_game()