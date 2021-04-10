class Board:
    def __init__(self, size: tuple):
        self.col = size[0]
        self.row = size[1]
        self.placeholder = '_' * len(str(self.col * self.row))
        self.placeholder_len = len(self.placeholder)
        self.adjust = ' ' * (self.placeholder_len - 1)
        self.board = {(x, y): self.placeholder for y in range(self.row, 0, -1) for x in range(1, self.col + 1)}

    def draw_board(self):
        print(' ---', '-' * (self.placeholder_len + 1) * self.col, sep='')
        for y in range(self.row, 0, -1):
            print(' ' * (len(str(self.row)) - len(str(y))), y, '| ', sep='', end='')
            print(*[''.join(self.board[x, y]) for x in range(1, self.col + 1)], end=" |\n")
        print(' ---', '-' * (self.placeholder_len + 1) * self.col, sep='')
        print('  ', *[' ' * self.placeholder_len + str(i) for i in range(1, self.col + 1)], sep='')

    def place_knight(self, cell: tuple):
        self.board[cell] = self.adjust + 'X'
        self.clean_board()
        _ = self.count_moves(cell)

    def count_moves(self, cell: tuple, deph: int = 2) -> int:
        if deph == 0:
            return 0
        deph -= 1
        count = 0
        col, row = cell[0], cell[1]
        for i in (-2, -1, 1, 2):
            for j in (-2, -1, 1, 2):
                if abs(i) == abs(j):
                    continue
                if (col + j, row + i) in self.board.keys():
                    if self.board[(col + j, row + i)] != self.placeholder:
                        continue
                    count += 1
                    result = self.count_moves((col + j, row + i), deph)
                    if result:
                        self.board[(col + j, row + i)] = self.adjust + str(result)
        return count

    def clean_board(self):
        for k, v in self.board.items():
            try:
                int(v)
            except:
                continue
            self.board[k] = self.placeholder


class Game:
    def __init__(self):
        self.count = 1
        self.dimensions = self.dimensions_input()
        self.board = Board(self.dimensions)
        self.over = False

    def start(self):
        self.position = self.position_input()
        self.board.place_knight(self.position)
        while not self.over:
            self.board.draw_board()
            if len(self.possible_moves()) > 0:
                self.board.place_knight(self.move())
            else:
                self.game_over()

    def move(self):
        while True:
            try:
                col, row = map(int, input("Enter your next move: ").split())
                if (col, row) in self.possible_moves():
                    self.board.board[self.position] = self.board.adjust + '*'
                    self.position = col, row
                    self.count += 1
                    return col, row
                else:
                    raise ValueError
            except ValueError:
                print('Invalid move!')

    def possible_moves(self):
        moves = []
        col, row = self.position[0], self.position[1]
        for i in (-2, -1, 1, 2):
            for j in (-2, -1, 1, 2):
                if abs(i) == abs(j):
                    continue
                if (col + j, row + i) in self.board.board.keys():
                    if self.board.board[(col + j, row + i)] != self.board.adjust + '*':
                        moves.append((col + j, row + i))
        print(moves)
        return moves

    @staticmethod
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

    def position_input(self):
        while True:
            try:
                col, row = map(int, input("Enter the knight's starting position: ").split())
                if 0 < col <= self.dimensions[0] and 0 < row <= self.dimensions[1]:
                    return col, row
                else:
                    raise ValueError
            except ValueError:
                print('Invalid position!')

    def game_over(self):
        count = 0
        self.over = True
        for v in self.board.board.values():
            if v == self.board.adjust + '*':
                count += 1
        if count == (self.board.col * self.board.row) - 1:
            print('What a great tour! Congratulations!')
        else:
            print('No more possible moves!')
            print(f'Your knight visited {self.count} squares!')


def main():
    Game().start()


if __name__ == '__main__':
    main()
