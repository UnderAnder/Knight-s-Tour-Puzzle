class Board:
    SIZE = 8

    def __init__(self):
        self.table = {(x, y): '_' for y in range(self.SIZE, 0, -1) for x in range(1, self.SIZE + 1)}

    def draw_board(self, cell):
        board = self.table
        board[cell] = 'X'
        print("""
 -------------------
8| {} {} {} {} {} {} {} {} |
7| {} {} {} {} {} {} {} {} |
6| {} {} {} {} {} {} {} {} |
5| {} {} {} {} {} {} {} {} |
4| {} {} {} {} {} {} {} {} |
3| {} {} {} {} {} {} {} {} |
2| {} {} {} {} {} {} {} {} |
1| {} {} {} {} {} {} {} {} |
 -------------------
   1 2 3 4 5 6 7 8
""".format(*board.values()))


def user_input():
    try:
        col, row = map(int, input("Enter the knight's starting position: ").split())
        if 0 < col < 9 and 0 < row < 9:
            return col, row
        else:
            raise ValueError
    except ValueError:
        print('Invalid dimensions!')
        exit()


def main():
    board = Board()
    board.draw_board(user_input())


if __name__ == '__main__':
    main()
