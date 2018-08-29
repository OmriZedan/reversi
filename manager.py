from board import *
from disk import Disk


class Manager:
    """this class is familiar with the dynamics and the rules of the game.
    changes done to the board and interaction between board and player are done via this class"""

    def is_valid_move(self, board, move, color):
        x_initial = move[0]
        y_initial = move[1]

        if board.get_cel(move) != Disk.NONE or not board.is_on_board(move):
            return False

        if color == Disk.DARK:
            opponent = Disk.LIGHT
        else:
            opponent = Disk.DARK

        for x_direction, y_direction in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x = x_initial + x_direction
            y = y_initial + y_direction
            pos = (x, y)
            if not board.is_on_board(pos) or board.get_cel(pos) != opponent:
                continue

            pos = (x + x_direction, y + y_direction)  # proceed in this direction
            if not board.is_on_board(pos):
                continue  # edge reached : no move can be done in this dirction

            # proceed further in this direction as long as there are opponent disks
            while board.get_cel(pos) == opponent:
                pos = (pos[0] + x_direction, pos[1] + y_direction)
                if not board.is_on_board(pos):
                    break
            if not board.is_on_board(pos):
                continue

            # if series ends with one of our disks: this is a valid move
            if board.get_cel(pos) == color:
                return True

        return False

    def get_possible_moves(self, board, color):
        """:returns: a list of possible moves, each move is a tuple of coordinates (x, y)."""
        N = len(board.data)
        moves = []
        for i in range(N):
            for j in range(N):
                move = (i, j)
                if self.is_valid_move(board, move, color):
                    moves.append(move)
        if len(moves) == 0:
            return None
        return moves

    def disks_to_flip(self, board, move, color):
        x_initial = move[0]
        y_initial = move[1]

        if color == Disk.DARK:
            opponent = Disk.LIGHT
        else:
            opponent = Disk.DARK

        disks = []
        for x_direction, y_direction in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x = x_initial + x_direction
            y = y_initial + y_direction
            pos = (x, y)
            if not board.is_on_board(pos) or board.get_cel(pos) != opponent:
                continue

            pos = (x + x_direction, y + y_direction)  # proceed in this direction
            if not board.is_on_board(pos):
                continue  # edge reached : no move can be done in this dirction

            # proceed further in this direction as long as there are opponent disks
            while board.get_cel(pos) == opponent:
                pos = (pos[0] + x_direction, pos[1] + y_direction)
                if not board.is_on_board(pos):
                    break
            if not board.is_on_board(pos):
                continue

            # if series ends with one of my disks: flip all the opponent disks in the way
            if board.get_cel(pos) == color:
                # go back to the initial disk, flipping disks in the way
                pos = (pos[0] - x_direction, pos[1] - y_direction)
                while board.get_cel(pos) == opponent:
                    disks.append(pos)
                    pos = (pos[0] - x_direction, pos[1] - y_direction)
        disks.append(move)
        return disks

    def change_cel(self, board, pos, color):
        board.change_cel(pos, color)

    def play_move(self, board, move, color):
        disks = self.disks_to_flip(board, move, color)
        for disk in disks:
            self.change_cel(board, disk, color)

    def is_game_over(self, board):
        possible_moves = self.get_possible_moves(board, Disk.DARK)
        if possible_moves is not None:
            return False
        possible_moves = self.get_possible_moves(board, Disk.LIGHT)
        if possible_moves is not None:
            return False
        return True

if __name__ == '__main__':
    b = Board(8)
    man = Manager()
    moves = man.get_possible_moves(b, Disk.DARK)
    print(f"possible moves: {moves}")
    moves = man.get_possible_moves(b, Disk.LIGHT)
    print(f"possible moves: {moves}")
