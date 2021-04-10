from collections import defaultdict


class Board:
    move_offsets = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))

    def __init__(self, size: tuple):
        self.col = size[0]
        self.row = size[1]
        self.placeholder = '_' * len(str(self.col * self.row))
        self.placeholder_len = len(self.placeholder)
        self.adjust = ' ' * (self.placeholder_len - 1)
        self.board = {(x, y): self.placeholder for y in range(self.row, 0, -1) for x in range(1, self.col + 1)}
        self.solve_list = list()

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
        self.set_moves_count(cell)

    def legal_moves_for(self, position):
        moves = []
        for i, j in self.move_offsets:
            cell = position[0] + j, position[1] + i
            if cell in self.board.keys():
                if self.board.get(cell) != self.adjust + '*':
                    moves.append(cell)
        return moves

    def legal_moves_count(self, position):
        moves = defaultdict(int)
        for i, j in self.legal_moves_for(position):
            moves[i, j] = len(self.legal_moves_for((i, j)))
        return moves

    def set_moves_count(self, position: tuple):
        for k, v in self.legal_moves_count(position).items():
            self.board[k] = f'{self.adjust}{v}'

    def clean_board(self):
        for k, v in self.board.items():
            try:
                int(v)
            except ValueError:
                continue
            self.board[k] = self.placeholder


class Game:
    def __init__(self):
        self.moves_count = 1
        self.dimensions = self.dimensions_input()
        self.board = Board(self.dimensions)
        self.position = self.position_input()
        self.over = False

    def start(self):
        self.board.place_knight(self.position)
        self.game_mode()

    def move(self):
        while True:
            try:
                col, row = map(int, input("Enter your next move: ").split())
                if (col, row) in self.board.legal_moves_for(self.position):
                    self.board.board[self.position] = self.board.adjust + '*'
                    self.position = col, row
                    self.moves_count += 1
                    return col, row
                else:
                    raise ValueError
            except ValueError:
                print('Invalid move!', end='')

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
            count += 1 if v == self.board.adjust + '*' else 0
        if count == (self.board.col * self.board.row) - 1:
            print('What a great tour! Congratulations!')
        else:
            print('No more possible moves!', f'Your knight visited {self.moves_count} squares!', sep='\n')

    def game_mode(self):
        while True:
            choice = input('Do you want to try the puzzle? (y/n): ')
            if choice == 'y':
                self.play_game()
                return
            elif choice == 'n':
                self.solution()
                return

    def play_game(self):
        while not self.over:
            self.board.draw_board()
            if len(self.board.legal_moves_for(self.position)) > 0:
                self.board.place_knight(self.move())
            else:
                self.game_over()

    def solution(self):
        pass


if __name__ == '__main__':
    Game().start()
