from abstract_player import AbstractPlayer
from board import Board
from cli import CLI
import re
letters = {chr(x): (x - ord('a')) for x in range(ord('a'), ord('z'))}
move_regx = re.compile(r"(\d),([a-z])")

class HumanPlayer(AbstractPlayer):
    """represents an interactive player (input output functions are determined by the choosen console)"""

    def message(self, possible_moves):
        message = f"{self}: it's your move\nYore possible moves are:"
        for (x, y) in possible_moves:
            y2 = chr(y + ord('a'))
            message += f"({x + 1},{y2}), "
        message += f"\b\nPlease choose your move row,col: "
        return message

    def set_console(self, console):
        self.console = console

    def get_move(self, board, possible_moves):
        """get move from player through interaction with console"""
        move = self.console.input(self.message(possible_moves))
        move = move_regx.search(move)
        x = int(move[1]) - 1
        y = ord(move[2]) - ord('a')

        return (x, y)