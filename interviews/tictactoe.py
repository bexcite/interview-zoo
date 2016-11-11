import random
import time


class TicTacToe(object):

    def __init__(self):
        self.board = [[' ', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
        self.player = True  # True = X, False = O

    def check(self):
        def is_solved(s):
            s = set(s)
            if len(s) == 1:
                p = s.pop()
                if p != ' ':
                    return p

        # Check rows
        for row in self.board:
            p = is_solved(row)
            if p:
                return p

        # Check columns
        for i in range(3):
            p = is_solved(self.board[j][i] for j in range(3))
            if p:
                return p

        # Check diagonals
        p = is_solved(self.board[i][i] for i in range(3))
        if p:
            return p
        p = is_solved(self.board[2 - i][i] for i in range(3))
        if p:
            return p

    def turn(self):
        p = self.check()
        if p:
            print 'Player %s has already won!' % p
        empty_slots = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    empty_slots.append((i, j))
        if not empty_slots:
            print 'No more moves!'
        slot = random.choice(empty_slots)
        # Place the move
        self.board[slot[0]][slot[1]] = self.piece()
        self.player = not self.player

    def piece(self):
        return 'X' if self.player else 'O'

    def print_board(self):
        print '-------'
        for row in self.board:
            print '|%s|%s|%s|' % tuple(row)
            print '-------'


if __name__ == '__main__':
    t = TicTacToe()

    while not t.check():
        print 'Player %s turn now...' % t.piece()
        t.turn()
        t.print_board()
        time.sleep(0.5)
    t.turn()
