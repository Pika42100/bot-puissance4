# bot_player.py

import random

class BotPlayer:
    def __init__(self, game):
        self.game = game

    def play(self):
        # Stratégie simple : essayer de gagner ou de bloquer l'adversaire
        for col in range(self.game.BOARD_WIDTH):
            if self.game.play(col):
                if self.game.check_win():
                    return col
                self.game.board[self.game.BOARD_HEIGHT - 1][col] = 0  # Annuler le coup

        # Si aucune victoire possible, jouer aléatoirement
        valid_columns = [col for col in range(self.game.BOARD_WIDTH) if self.game.board[0][col] == 0]
        if valid_columns:
            column = random.choice(valid_columns)
            self.game.play(column)
            return column
        return None
