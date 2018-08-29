from abstract_player import AbstractPlayer
from copy import deepcopy
from disk import Disk
from datetime import datetime
## for imports for testing purposes
from board import Board
from manager import Manager
from cli import CLI

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
        for depth in range(2,3):   # iterative deepening
            try:
                for move in possible_moves:
                    board_copy = deepcopy(board)
                    self.man.play_move(board_copy, move, self.color)
                    score = self.minimaxm(depth, board, False)
                    if score > max_score:
                        max_score = score
                        next_move = move

            except TimeoutError:
                print("ran out of time")
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

        if self.color == Disk.DARK:
            opponent = Disk.LIGHT
        else:
            opponent = Disk.DARK

        # end recursion
        if self.man.is_game_over(board) or depth == 0:
            return self.calc_score3(board, self.color)

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
                if self.time_per_turn - elapsed_time < 0.001:
                    raise TimeoutError

                board_copy = deepcopy(board)
                self.man.play_move(board_copy, move, self.color)
                score = self.minimaxm(depth - 1, board_copy, not maximizer)
                score += 0.2 * (self.mobility(board, self.color, opponent))
                if score > max_score:
                    max_score = score

            return max_score

        # minimizer turn
        else:
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
                score += 0.2 * (self.mobility(board, self.color, opponent))
                if score < min_score:
                    min_score = score

            return min_score

    def calc_score3(self, board, color):
        N = len(board.data)
        score = 0
        for i in range(N):
            for j in range(N):
                pos = (i, j)
                disk = board.get_cel(pos)
                if disk == Disk.DARK:
                    score += self.weights_matrix[i][j]
                elif disk == Disk.LIGHT:
                    score -= self.weights_matrix[i][j]
        return score

    def weights(self,negative_weight=-50):
        weights_matrix =  [[ 50,     -50,     50,     30,    30,     50,     -50,    50],
                           [-50,     -50,    -30,      1,     1,    -30,     -50,   -50],
                           [ 30,     -30,      1,      1,     1,      1,     -30,    30],
                           [ 20,       1,      1,      1,     1,      1,       1,    20],
                           [ 20,       1,       1,     1,      1,     1,       1,    20],
                           [ 30,     -30,       1,     1,      1,     1,     -30,    30],
                           [-50,     -50,     -30,     1,      1,   -30,     -50,   -50],
                           [ 50,     -50,      50,    30,     30,     50,    -50,    50]
                           ]
        return weights_matrix

    def set_minimax_variables(self, man):
        self.weights_matrix = self.weights()
        self.man = man

#########################################################################################################
#########################################################################################################
#########################################################################################################
    def calc_score(self,board, color):
        if self.color == Disk.DARK:
            opponent = Disk.LIGHT
        else:
            opponent = Disk.DARK
        cp = self.coin_parity(board, self.color, opponent)
        cc = self.corners_captured(board, self.color, opponent)
        ed = self.edges(board, self.color, opponent)
        return 3 * cp + 4 * cc + ed

    def coin_parity(self, board, color, opponent):
        """:returns the relative difference in disk between the max player and the min player"""
        stats = board.stats()
        return stats[color] - stats[opponent]

    def corners_captured(self, board, color, opponent):
        """
        :returns the relative difference in corners captured by the max player and those captured by the min player.
        Corners hold special importance because once captured
        """
        corners = board.corners()
        max_player_corners = corners[color]
        min_player_corners = corners[opponent]
        if  max_player_corners + min_player_corners == 0:
            return 0
        return max_player_corners - min_player_corners





#########################################################################################################
#########################################################################################################
#########################################################################################################
    def edges(self, board, color, opponent):
        edges = board.edges()
        return edges[color] - edges[opponent]


#########################################################################################################
#########################################################################################################
#########################################################################################################

    def calc_score2(self, board, color, opponent):
        stats = board.stats()
        return stats[color] - stats[opponent]

    def mobility(self, board, color, opponent):
        """:returns the relative difference between the number of possible moves for the max and the min players"""
        max_player_possible_moves = self.man.get_possible_moves(board, color)
        min_player_possible_moves = self.man.get_possible_moves(board, opponent)
        if max_player_possible_moves:
            max_player_moves = len(self.man.get_possible_moves(board, color))
        else:
            max_player_moves = 0

        if min_player_possible_moves:
            min_player_moves = len(self.man.get_possible_moves(board, opponent))
        else:
            min_player_moves = 0

        if max_player_moves + min_player_moves == 0:
            return 0

        return max_player_moves - min_player_moves

#########################################################################################################
#########################################################################################################
#########################################################################################################
def vulnerability(self, board, color, opponent):
        """
        :returns the relative difference between players' disks of in immediate danger of being flipped
        this represents the player's vulnerability
        """
        max_possible_moves = self.man.get_possible_moves(board, color)
        min_possible_moves = self.man.get_possible_moves(board, opponent)
        max_disks = set()
        min_disks = set()
        if max_possible_moves:
            for move in max_possible_moves:
                max_disks.update(set(self.man.disks_to_flip(board, move, color)))
            min_player_vulnerable_disks = len(max_disks) - len(max_possible_moves)
        else:
            min_player_vulnerable_disks = 0

        if min_possible_moves:
            for move in min_possible_moves:
                min_disks.update(set(self.man.disks_to_flip(board, move, opponent)))
            max_player_vulnerable_disks = len(min_disks) - len(min_possible_moves)
        else:
            max_player_vulnerable_disks = 0

        if max_player_vulnerable_disks + min_player_vulnerable_disks == 0:
            return 0
        return 100 * (min_player_vulnerable_disks - max_player_vulnerable_disks) / (min_player_vulnerable_disks + max_player_vulnerable_disks)

if __name__ == '__main__':
    b = Board(8)
    p1 = Player02(Disk.DARK)
    man = Manager()
    console = CLI()
    b.change_cel((0, 0), Disk.DARK)
    p1.set_manager(man)
    p1_moves = p1.man.get_possible_moves(b, Disk.DARK)
    p1.man.play_move(b, p1_moves[0], Disk.DARK)

    console.display_board(b)

    ## testing board-evaluation sub methods:

    cp = p1.coin_parity(b, Disk.DARK, Disk.LIGHT)
    print(cp)
    # m = p1.mobility(b, Disk.DARK, Disk.LIGHT)
    # print(m)
    cc = p1.corners_captured(b, Disk.DARK, Disk.LIGHT)
    print(cc)
    score = p1.calc_score(b, Disk.DARK)
    print("score:", score)

    print('\n\n')
    b.change_cel((4, 2), Disk.DARK)
    console.display_board(b)

    cp = p1.coin_parity(b, Disk.DARK, Disk.LIGHT)
    print(cp)
    # m = p1.mobility(b, Disk.DARK, Disk.LIGHT)
    # print(m)
    cc = p1.corners_captured(b, Disk.DARK, Disk.LIGHT)
    print(cc)
    score = p1.calc_score(b, Disk.DARK)
    print("score:", score)
