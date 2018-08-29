from abstract_player import AbstractPlayer
from copy import deepcopy
from disk import Disk

class SimplePlayer(AbstractPlayer):
    """
    represents a player with a simple decision making algorithm:
    the player chooses his move by evaluating the board ,given -hypothetically- the move was played
    """

    def get_move(self, board, possible_moves):
        """get best move ,in depth n"""

        max_score = -float('Inf')

        if self.color == Disk.DARK:
            opponent = Disk.LIGHT
        else:
            opponent = Disk.DARK

        for move in possible_moves:
            board_copy = deepcopy(board)
            self.man.play_move(board_copy, move, self.color)
            stats = board_copy.stats()
            score = stats[self.color] - stats[opponent]
            if score > max_score:
                max_score = score
                chosen_move = move

            return chosen_move

    def set_manager(self, man):
        """ SimplePlayer needs a manager to play hypothetical moves"""
        self.man = man
