import random
import socket
from secrets import compare_digest
from datetime import datetime


class Player:
    def __init__(self, name, count, player_socket):
        self.name = name
        self.count = count
        self.player_socket = player_socket

    def __str__(self):
        return f"{self.name}={self.count}"


class Game:
    def __init__(self, game_id, creator_player, game_type, game_password=""):
        self.creator_player = creator_player
        self.game_type = game_type
        self.white_player = None
        self.black_player = None
        self.is_game_start = False
        self.game_password = game_password
        self.game_id = game_id

    def __str__(self):
        return f"{self.creator_player.name}={self.game_type}={self.game_id}"

    def join(self, player, password=""):
        if self.game_type == "public":
            self.is_game_start = True
            return True
        elif self.game_type == "password":
            if compare_digest(password, self.game_password):
                self.is_game_start = True
                return True
        else:
            return False




def log(*log_str):
    st = ""
    for s in log_str:
        st += " " + str(s)
    f = open('log.txt', 'w')
    f.write(str(datetime.now()) + ':' + str(st) + '\n')
    f.close()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 5059))
client = []  # Массив где храним адреса клиентов

games = list()
not_started_games = []

print('Start Server')
while True:
    data, addres = sock.recvfrom(1024)
    dt_str = data.decode('utf-8')
    log(addres[0], addres[1], dt_str)

    dt = dt_str[2:].split('=')
    if dt_str[:2] == "#n":
        # "#n<name>=<count>=<game type>=<password if need>"
        if dt[2] == "password":
            g = Game(len(not_started_games), Player(dt[0], int(dt[1]), addres), dt[2], dt[3])
        else:
            g = Game(len(not_started_games), Player(dt[0], int(dt[1]), addres), dt[2])
        not_started_games.append(g)
        print("one more game")

    if dt_str[:2] == "#l":
        # "#l"
        stlg = ""
        for g in not_started_games:
            stlg += str(g)
            stlg += '&'
        stlg = "#l" + stlg[:-1]
        sock.sendto(stlg.encode('utf-8'), addres)

    if dt_str[:2] == "#j":
        # "#j<name>=<count>=<game id>=<password if need>"
        if not_started_games[int(dt[2])].game_type == "password":
            r = not_started_games[int(dt[2])].join(Player(dt[0], int(dt[1]), addres), dt[3])
        else:
            r = not_started_games[int(dt[2])].join(Player(dt[0], int(dt[1]), addres))

        if r:
            games.append(not_started_games[int(dt[2])])
            games[len(games) - 1].game_id = len(games) - 1
            gi = len(games) - 1
            if random.choice([True, False]):

                games[gi].white_player = games[gi].creator_player
                games[gi].black_player = Player(dt[0], int(dt[1]), addres)
                sock.sendto(
                    f"#*start={str(not_started_games[int(dt[2])])}={dt[0]}={dt[1]}={gi}".encode('utf-8'),
                    not_started_games[int(dt[2])].creator_player)
                sock.sendto(
                    f"#*start={str(not_started_games[int(dt[2])])}={dt[0]}={dt[1]}={gi}".encode('utf-8'),
                    addres)
            else:
                games[gi].black_player = games[gi].creator_player
                games[gi].white_player = Player(dt[0], int(dt[1]), addres)
                sock.sendto(
                    f"#*start={dt[0]}={dt[1]}={str(not_started_games[int(dt[2])])}={gi}".encode('utf-8'),
                    not_started_games[int(dt[2])].creator_player)
                sock.sendto(
                    f"#*start={dt[0]}={dt[1]}={str(not_started_games[int(dt[2])])}={gi}".encode('utf-8'),
                    addres)

            not_started_games[int(dt[2])] = None

        else:
            sock.sendto(f"#*not".encode('utf-8'), addres)

    if dt_str[:2] == "#$":
        # "#$<from x>=<from y>=<to x>=<to y>=<game id>"
        if games[int(dt[4])].white_player == addres:
            sock.sendto(data, games[int(dt[4])].black_player)
        else:
            sock.sendto(data, games[int(dt[4])].white_player)

    if dt_str[:2] == "#$":
        # "#$<game id>"
        games[int(dt[0])] = None

    if addres not in client:
        client.append(addres)  # Если такого клиента нету , то добавить
    for clients in client:
        if clients == addres:
            continue  # Не отправлять данные клиенту, который их прислал
        sock.sendto(data, clients)
