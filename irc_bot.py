import socket
import threading
import logging
from config import IRC_SERVER, IRC_PORT, IRC_CHANNEL, IRC_NICK, IRC_PASSWORD
from puissance4 import Puissance4
from bot_player import BotPlayer

class IRCBot:
    def __init__(self):
        self.server = IRC_SERVER
        self.port = IRC_PORT
        self.channel = IRC_CHANNEL
        self.nick = IRC_NICK
        self.password = IRC_PASSWORD
        self.game = Puissance4()
        self.bot_player = BotPlayer(self.game)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.sock.connect((self.server, self.port))
            self.sock.send(f"NICK {self.nick}\r\n".encode())
            self.sock.send(f"USER {self.nick} 0 * :{self.nick}\r\n".encode())
            if self.password:
                self.sock.send(f"PASS {self.password}\r\n".encode())
            self.sock.send(f"JOIN {self.channel}\r\n".encode())
            logging.info("Connected to IRC server")
            self.listen()
        except Exception as e:
            logging.error(f"Failed to connect to IRC server: {e}")

    def listen(self):
        try:
            while True:
                data = self.sock.recv(4096).decode()
                if data:
                    logging.debug(f"Received data: {data}")
                    self.handle_message(data)
        except Exception as e:
            logging.error(f"Error in listen loop: {e}")

    def handle_message(self, data):
        if data.startswith("PING"):
            ping_message = data.split("PING :")[1].strip()
            self.sock.send(f"PONG :{ping_message}\r\n".encode())
            logging.debug(f"Sent PONG response: {ping_message}")
        elif "PRIVMSG" in data:
            message = data.split("PRIVMSG", 1)[1].split(":", 1)[1].strip()
            self.process_command(message)

    def process_command(self, message):
        if message.startswith("!play"):
            try:
                column = int(message.split()[1])
                if self.game.play(column):
                    self.sock.send(f"PRIVMSG {self.channel} :Jeton placé dans la colonne {column}\r\n".encode())
                    self.send_board()
                    if self.game.check_win():
                        self.sock.send(f"PRIVMSG {self.channel} :Vous avez gagné!\r\n".encode())
                        self.game.reset()
                        self.send_board()
                    else:
                        bot_column = self.bot_player.play()
                        self.sock.send(f"PRIVMSG {self.channel} :Le bot joue dans la colonne {bot_column}\r\n".encode())
                        self.send_board()
                        if self.game.check_win():
                            self.sock.send(f"PRIVMSG {self.channel} :Le bot a gagné!\r\n".encode())
                            self.game.reset()
                            self.send_board()
                else:
                    self.sock.send(f"PRIVMSG {self.channel} :Colonne invalide ou pleine.\r\n".encode())
            except (IndexError, ValueError):
                self.sock.send(f"PRIVMSG {self.channel} :Commande invalide. Utilisez !play <colonne>.\r\n".encode())
        elif message.startswith("!board"):
            self.send_board()
        elif message.startswith("!reset"):
            self.game.reset()
            self.sock.send(f"PRIVMSG {self.channel} :Le jeu a été réinitialisé.\r\n".encode())
            self.send_board()
        elif message.startswith("!rules"):
            self.sock.send(f"PRIVMSG {self.channel} :Les règles du jeu de Puissance 4 sont simples. Chaque joueur place un jeton dans une colonne. Le premier joueur à aligner 4 jetons horizontalement, verticalement ou en diagonale gagne.\r\n".encode())

    def send_board(self):
        board_str = self.game.get_board_str()
        for line in board_str.split("\n"):
            self.sock.send(f"PRIVMSG {self.channel} :{line}\r\n".encode())

if __name__ == "__main__":
    logging.basicConfig(filename='irc_bot.log', level=logging.DEBUG)
    bot = IRCBot()
    bot.connect()
