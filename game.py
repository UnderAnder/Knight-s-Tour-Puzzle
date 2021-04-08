class Board:
    def __init__(self, size):
        self.col = size[0]
        self.row = size[1]
        self.placeholder = '_' * len(str(self.col * self.row))
        self.table = {(x, y): self.placeholder for y in range(self.row, 0, -1) for x in range(1, self.col + 1)}

    def draw_board(self, cell):
        board = self.table
        board[cell] = ' ' * len(self.placeholder[:-1]) + 'X'
        print(' ---', '-' * (len(self.placeholder) + 1) * self.col, sep='')
        for y in range(self.row, 0, -1):
            print(' ' * (len(str(self.row)) - len(str(y))), y, '| ', sep='', end='')
            for x in range(1, self.col + 1):
                print(board[x, y], '', end='')
            print('|')
        print(' ---', '-' * (len(self.placeholder) + 1) * self.col, sep='')
        print('  ', *[' ' * (len(self.placeholder)) + str(i) for i in range(1, self.col + 1)], sep='')


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
    board.draw_board(position_input(dimensions))


if __name__ == '__main__':
    main()
