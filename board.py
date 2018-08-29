from disk import Disk
symbols = {Disk.NONE: " ", Disk.DARK: "X", Disk.LIGHT: "O"}
class Board:
    """represents an N X N reversi board
    cells values can take each of the enum Disk values"""

    def __init__(self, N, data = None):
        if data is None:
            self.data = []
            for i in range(N):
                row = [Disk.NONE] * N
                self.data.append(row)
            # default game start
            self.N = N
            center1 = (self.N // 2, self.N // 2)
            center2 = ((self.N // 2) - 1, self.N // 2)
            center3 = (self.N // 2, (self.N // 2) - 1)
            center4 = ((self.N // 2) - 1, (self.N // 2) - 1)

            self.change_cel(center1, Disk.DARK)
            self.change_cel(center2, Disk.LIGHT)
            self.change_cel(center3, Disk.LIGHT)
            self.change_cel(center4, Disk.DARK)

        else:
            self.data = data
            self.N = len(data)



    def get_cel(self, pos):
        x = pos[0]
        y = pos[1]

        if x < self.N and y < self.N:
            return self.data[x][y]
        raise IndexError("Index out of bounds")

    def change_cel(self, pos, value):
        """ :param pos: an (x, y) tuple representing the position on the board
            :param value: the new value
        """
        x = pos[0]
        y = pos[1]
        self.data[x][y] = value

    def __str__(self):
        return_string = ""
        for row in self.data:
            for cel in row:
                return_string += f" {symbols[cel]} "
            return_string += "\n"

        return return_string

    def is_on_board(self, pos):
        """check if a position is on the board"""
        x = pos[0]
        y = pos[1]
        N = len(self.data)
        if x < 0 or x >= N or y < 0 or y >= N:
            return False
        return True

    def stats(self):
        """:returns dictionary of disk color and redundancy.
         i.e. dict[Disk.DARK]: number of dark disks on board"""
        N = len(self.data)
        dark_disks, light_disks = 0, 0
        for i in range(N):
            for j in range(N):
                pos = (i, j)
                if self.get_cel(pos) == Disk.DARK:
                    dark_disks += 1
                elif self.get_cel(pos) == Disk.LIGHT:
                    light_disks += 1
        return {Disk.DARK: dark_disks, Disk.LIGHT: light_disks}

if __name__ == '__main__':
    b = Board(8)
    print(b.data[0][5])
    b.data[0][5] = -1
    print(b.data[0][5])
    print(b.data[1][5])
