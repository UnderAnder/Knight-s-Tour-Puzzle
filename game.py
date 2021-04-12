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

    def draw_board(self):
        print(' ---', '-' * (self.placeholder_len + 1) * self.col, sep='')
        for y in range(self.row, 0, -1):
            print(' ' * (len(str(self.row)) - len(str(y))), y, '| ', sep='', end='')
            print(*[''.join(self.board[x, y]) for x in range(1, self.col + 1)], end=" |\n")
        print(' ---', '-' * (self.placeholder_len + 1) * self.col, sep='')
        print('  ', *[' ' * self.placeholder_len + str(i) for i in range(1, self.col + 1)], sep='')

    def place_knight(self, position: tuple):
        self.board[position] = self.adjust + 'X'
        self.set_moves_count(position)

    def solve(self, position: tuple, depth: int = 1):
        self.board[position] = ' ' * (self.placeholder_len - len(str(depth))) + str(depth)
        depth += 1
        if self.check_end(position):
            if self.get_result() == 'Win':
                return True
            else:
                self.board[position] = self.placeholder
                return False
        moves = self.legal_moves_count(position)
        for move in sorted(moves, key=moves.get):
            if self.solve(move, depth):
                return True
            else:
                self.board[move] = self.placeholder
                continue
        return False

    def legal_moves_for(self, position):
        moves = []
        for i, j in self.move_offsets:
            cell = position[0] + j, position[1] + i
            if cell in self.board.keys():
                if self.board[cell] == self.placeholder:
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

    def check_end(self, position):
        return True if len(self.legal_moves_for(position)) == 0 else False

    def get_result(self):
        count = 0
        for v in self.board.values():
            count += 1 if v == self.placeholder else 0
        return 'Win' if count == 0 else 'Lose'


class Game:
    position: tuple[int, int]

    def __init__(self):
        self.moves_count = 1
        self.dimensions = self.dimensions_input()
        self.board = Board(self.dimensions)
        self.position = self.position_input()
        self.over = False

    def start(self):
        while True:
            choice = input('Do you want to try the puzzle? (y/n): ')
            if choice == 'y':
                return self.play_game()
            elif choice == 'n':
                return self.solution()
            print('Invalid option')

    def play_game(self):
        if not self.board.solve(self.position):
            print('No solution exists!')
            exit()

        self.board.clean_board()
        self.board.place_knight(self.position)
        while not self.over:
            self.board.draw_board()
            self.board.clean_board()
            if not self.board.check_end(self.position):
                self.board.place_knight(self.move())
            else:
                self.game_over()

    def solution(self):
        if self.board.solve(self.position):
            print("Here's the solution!")
            self.board.draw_board()
        else:
            print('No solution exists!')

    def move(self):
        while True:
            try:
                col, row = map(int, input("Enter your next move: ").split())
                self.board.clean_board()
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
        self.over = True
        win_message = 'What a great tour! Congratulations!'
        lose_message = f'No more possible moves\nYour knight visited {self.moves_count} squares!'
        print(win_message if self.board.get_result() == 'Win' else lose_message)


if __name__ == '__main__':
    Game().start()
