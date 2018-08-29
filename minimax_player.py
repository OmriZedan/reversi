from abstract_player import AbstractPlayer
from copy import deepcopy
from disk import Disk
from datetime import datetime

class Player02(AbstractPlayer):
    """
    represents a player with a MINIMAX decision making algorithm:
    the player chooses his move by recursively evaluating the board according to MINIMAX algorithm
    """

    def get_move(self, board, possible_moves):
        """get best move ,in depth n"""

        next_move = None
        max_score = -float('Inf')
        self.start_time = datetime.now()
        for depth in range(3,10):   # iterative deepening
            try:
                for move in possible_moves:
                    score = self.minimaxm(depth, board, True)
                    if score > max_score:
                        max_score = score
                        next_move = move

            except TimeoutError:
               break

        return next_move

    def minimaxm(self, depth, board, maximizer):
        """
        :param board: board to assess
        :param color: maximizer player color
        :param opponent_color: minimizer player color
        :param maximizer: role(maximizer or minimizer ?) True = maximizer, False = minimizer
        :return: score - score is calculated according to external function calc_score()
        """
        # end recursion
        if self.man.is_game_over(board) or depth == 0:
            return self.calc_score(board, self.color)

        # time check
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        if self.time_per_turn - elapsed_time < 0.0001:
            raise TimeoutError

        # maximizer turn
        if maximizer:
            # player out of moves. call minimax on opponent
            possible_moves = self.man.get_possible_moves(board, self.color)
            if possible_moves is None:
                return self.minimaxm(depth - 1, board, not maximizer)

            max_score = -float('Inf')
            for move in possible_moves:

                # time check
                elapsed_time = (datetime.now() - self.start_time).total_seconds()
                if self.time_per_turn - elapsed_time < 0.0001:
                    raise TimeoutError

                board_copy = deepcopy(board)
                self.man.play_move(board_copy, move, self.color)
                score = self.minimaxm(depth - 1, board_copy, not maximizer)
                if score > max_score:
                    max_score = score

            return max_score

        # minimizer turn
        else:

            if self.color == Disk.DARK:
                opponent = Disk.LIGHT
            else:
                opponent = Disk.DARK

            # opponent out of moves. call minimax on player
            possible_moves = self.man.get_possible_moves(board, opponent)
            if possible_moves is None:
                return self.minimaxm(depth - 1, board, not maximizer)

            min_score = float('Inf')
            for move in possible_moves:

                # time check
                elapsed_time = (datetime.now() - self.start_time).total_seconds()
                if self.time_per_turn - elapsed_time < 0.0001:
                    raise TimeoutError

                board_copy = deepcopy(board)
                self.man.play_move(board_copy, move, opponent)
                score = self.minimaxm(depth - 1, board_copy, not maximizer)
                if score < min_score:
                    min_score = score

            return min_score

    def calc_score(self,board, color):
        if self.color == Disk.DARK:
            opponent = Disk.LIGHT
        else:
            opponent = Disk.DARK
        stats = board.stats()
        return stats[self.color] - stats[opponent]

    def set_manager(self, man):
        """ minimax player needs a manager to play hypothetical moves"""
        self.man = man