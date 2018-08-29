from abstract_player import AbstractPlayer
import random

class RandomPlayer(AbstractPlayer):
    def __init__(self, color):
        super().__init__(color)

    def get_move(self, board, possible_moves):
        index = random.randint(0, len(possible_moves) - 1)
        return possible_moves[index]