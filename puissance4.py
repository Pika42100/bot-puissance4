# puissance4.py

from config import BOARD_WIDTH, BOARD_HEIGHT, WINNING_LENGTH

class Puissance4:
    def __init__(self):
        self.BOARD_WIDTH = BOARD_WIDTH
        self.BOARD_HEIGHT = BOARD_HEIGHT
        self.WINNING_LENGTH = WINNING_LENGTH
        self.board = [[0] * self.BOARD_WIDTH for _ in range(self.BOARD_HEIGHT)]
        self.current_player = 1

    def play(self, column):
        if column < 0 or column >= self.BOARD_WIDTH:
            return False
        for row in range(self.BOARD_HEIGHT - 1, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                self.current_player = 3 - self.current_player  # Switch player (1 <-> 2)
                return True
        return False

    def check_win(self):
        for row in range(self.BOARD_HEIGHT):
            for col in range(self.BOARD_WIDTH):
                if self.board[row][col] != 0:
                    if self.check_direction(row, col, 1, 0) or \
                       self.check_direction(row, col, 0, 1) or \
                       self.check_direction(row, col, 1, 1) or \
                       self.check_direction(row, col, 1, -1):
                        return True
        return False

    def check_direction(self, row, col, d_row, d_col):
        player = self.board[row][col]
        count = 1
        for i in range(1, self.WINNING_LENGTH):
            new_row, new_col = row + i * d_row, col + i * d_col
            if 0 <= new_row < self.BOARD_HEIGHT and 0 <= new_col < self.BOARD_WIDTH and self.board[new_row][new_col] == player:
                count += 1
            else:
                break
        for i in range(1, self.WINNING_LENGTH):
            new_row, new_col = row - i * d_row, col - i * d_col
            if 0 <= new_row < self.BOARD_HEIGHT and 0 <= new_col < self.BOARD_WIDTH and self.board[new_row][new_col] == player:
                count += 1
            else:
                break
        return count >= self.WINNING_LENGTH

    def get_board_str(self):
        board_str = ""
        for row in self.board:
            board_str += "|".join("X" if cell == 1 else "O" if cell == 2 else " " for cell in row) + "|\n"
        board_str += " " + " ".join(str(i) for i in range(self.BOARD_WIDTH)) + "\n"
        return board_str

    def reset(self):
        self.board = [[0] * self.BOARD_WIDTH for _ in range(self.BOARD_HEIGHT)]
        self.current_player = 1
