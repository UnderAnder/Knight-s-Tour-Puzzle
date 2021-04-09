class Board:
    def __init__(self, size: tuple):
        self.col = size[0]
        self.row = size[1]
        self.placeholder = '_' * len(str(self.col * self.row))
        self.placeholder_len = len(self.placeholder)
        self.board = {(x, y): self.placeholder for y in range(self.row, 0, -1) for x in range(1, self.col + 1)}

    def draw_board(self):
        print(' ---', '-' * (self.placeholder_len + 1) * self.col, sep='')
        for y in range(self.row, 0, -1):
            print(' ' * (len(str(self.row)) - len(str(y))), y, '| ', sep='', end='')
            print(*[''.join(self.board[x, y]) for x in range(1, self.col + 1)], end=" |\n")
        print(' ---', '-' * (self.placeholder_len + 1) * self.col, sep='')
        print('  ', *[' ' * self.placeholder_len + str(i) for i in range(1, self.col + 1)], sep='')

    def place_knight(self, cell: tuple):
        self.board[cell] = ' ' * (self.placeholder_len - 1) + 'X'
        _ = self.possible_moves(cell)

    def possible_moves(self, cell: tuple, deph: int = 2):
        if deph == 0:
            return
        deph -= 1
        count = -1
        col, row = cell[0], cell[1]
        for i in (-2, -1, 1, 2):
            for j in (-2, -1, 1, 2):
                if abs(i) == abs(j):
                    continue
                if (col + j, row + i) in self.board.keys():
                    count += 1
                    result = self.possible_moves((col + j, row + i), deph)
                    if result:
                        self.board[(col + j, row + i)] = ' ' * (self.placeholder_len - 1) + str(result)
        return count


def dimensions_input():
    while True:
        try:
            col, row = map(int, input("Enter your board dimensions: ").split())
            if col > 0 and row > 0:
                return col, row
            else:
                raise ValueError
        except ValueError:
            print('Invalid dimensions!')


def position_input(dimensions):
    while True:
        try:
            col, row = map(int, input("Enter the knight's starting position: ").split())
            if 0 < col <= dimensions[0] and 0 < row <= dimensions[1]:
                return col, row
            else:
                raise ValueError
        except ValueError:
            print('Invalid position!')


def main():
    dimensions = dimensions_input()
    board = Board(dimensions)
    board.place_knight(position_input(dimensions))
    board.draw_board()


if __name__ == '__main__':
    main()
