from disk import Disk
from board import Board

symbols = {Disk.NONE: " ", Disk.DARK: "X", Disk.LIGHT: "O"}

class CLI:

    def display_board(self, board):
        N = len(board.data)
        display = "   |"
        for i  in range(N):
            display += f" {chr(ord('a') + i)} |"

        display += "\n"
        for i in range(N):

            for j in range(N + 1):
                display += "---+"

            if i < 9:
                display += f"\n {i + 1} |"
            else:
                display += f"\n{i + 1} |"
            for j in range(N):
                pos = (i, j)
                display += f" {symbols[board.get_cel(pos)]} |"

            display += '\n'

        for j in range(N + 1):
            display += "---+"

        print(display)


    def print(self, message):
        print(message)

    def input(self, message):
        user_input = input(message)
        return user_input

    def newline(self):
        print("-" * 30)


if __name__ == '__main__':
    console = CLI()

    board = Board(8)
    print("\n\n\n\n")

    console.display_board(board)
