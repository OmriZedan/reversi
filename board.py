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

    def corners(self):
        """:returns dictionary of disk color and how many corners does it occupy"""
        N = len(self.data)
        dark_corners, light_corners = 0, 0
        for i in range(0, N, N-1):
            for j in range(0, N, N - 1):
                if self.data[i][j] == Disk.DARK:
                    dark_corners += 1
                elif self.data[i][j] == Disk.LIGHT:
                    light_corners += 1
        return {Disk.DARK: dark_corners, Disk.LIGHT: light_corners}

    def edges(self):
        """:returns dictionary of disk color and how many disks are on the edges"""
        N = len(self.data)
        dark_disks, light_disks = 0, 0

        for i in range(N):#upper edge
                if self.data[0][i] == Disk.DARK:
                    dark_disks += 1
                elif self.data[0][i] == Disk.LIGHT:
                    light_disks += 1

        for i in range(N):#bottom edge
            if self.data[N - 1][i] == Disk.DARK:
                dark_disks += 1
            elif self.data[N - 1][i] == Disk.LIGHT:
                light_disks += 1

        for i in range(N):#right edge
            if self.data[i][N -1 ] == Disk.DARK:
                dark_disks += 1
            elif self.data[i][N - 1] == Disk.LIGHT:
                light_disks += 1

        for i in range(N):#left edge
            if self.data[i][0] == Disk.DARK:
                dark_disks += 1
            elif self.data[i][0] == Disk.LIGHT:
                light_disks += 1
        return {Disk.DARK: dark_disks, Disk.LIGHT: light_disks}

    def stable_disks(self):
        """
        :returns dictionary of disk color and how many of them are stable
        stable disk : cannot be flipped by opponent
        """
        dark_stable_disks, light_stable_disks = 0, 0
        return {Disk.DARK: dark_stable_disks, Disk.LIGHT: light_stable_disks}

    def vulnerable_disks(self):
        """
        :returns dictionary of disk color and how many of them are stable
        semi-stable disk : can be flipped by opponent in the next move
        """

        dark_vulnerable_disks, light_vulnerable_disks = 0, 0
        return {Disk.DARK: dark_vulnerable_disks, Disk.LIGHT: light_vulnerable_disks}

if __name__ == '__main__':
    b = Board(8)
    print(b.data[0][5])
    b.change_cel((0,0), Disk.DARK)
    b.change_cel((7,0), Disk.DARK)
    b.change_cel((0,7), Disk.DARK)
    b.change_cel((7,7), Disk.DARK)
    corners = b.corners()
    print(corners[Disk.DARK])