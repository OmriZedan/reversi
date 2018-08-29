from cli import CLI
from board import Board
from manager import Manager
from disk import Disk
from abstract_player import AbstractPlayer
from random_player import RandomPlayer
from human_player import HumanPlayer
from simple_player import SimplePlayer
from minimax_player import Player02

class Runner:
    """runs the game"""
    def __init__(self, board_size=8, player1_type=HumanPlayer, player2_type=HumanPlayer):
        self.console = CLI()
        self.board = Board(board_size)
        self.manager = Manager()

        self.p1 = player1_type(Disk.DARK)
        if issubclass(player1_type, HumanPlayer):
            self.p1.set_console(self.console)
        if issubclass(player1_type, SimplePlayer):
            self.p1.set_manager(self.manager)
        if issubclass(player1_type, Player02):
            self.p1.set_minimax_variables(self.manager)

        self.p2 = player2_type(Disk.LIGHT)
        if issubclass(player2_type, HumanPlayer):
            self.p2.set_console(self.console)
        if issubclass(player2_type, SimplePlayer) or issubclass(player2_type, Player02):
            self.p2.set_manager(self.manager)
        if issubclass(player2_type, Player02):
            self.p2.set_minimax_variables(self.manager)

        self.current_player = self.p1

    def run_game(self):
        console = self.console
        board = self.board
        man = self.manager

        # console.display_board(board)
        # console.newline()

        while True:
            moves = man.get_possible_moves(board, self.current_player.color)
            if moves is None:
                self.switch_player()
                moves = man.get_possible_moves(board, self.current_player.color)
                if moves is None:
                    break

            move = self.current_player.get_move(board, moves)
            man.play_move(board, move, self.current_player.color)
            # self.console.display_board(board)
            # console.newline()
            self.switch_player()

        message, winner = self.evaluate_game()
        print(message)
        return  winner

    def switch_player(self):
        """switches the current player"""
        if self.current_player == self.p1:
            self.current_player = self.p2
        else:
            self.current_player = self.p1

    def evaluate_game(self):
        """
        run after the game is over
        :returns a string containing the result
        """
        points = self.board.stats()
        points_p1, points_p2 = points[self.p1.color], points[self.p2.color]
        message = f"{self.p1}:{points_p1} --- {self.p2}:{points_p2}\n"
        if points_p1 > points_p2:
            message += f"{self.p1} WINS"
            winner = self.p1.color
        elif points_p1 < points_p2:
            message += f"{self.p2} WINS"
            winner = self.p2.color
        else:
            message += f"It's a DRAW'"
            winner = None

        return message, winner

