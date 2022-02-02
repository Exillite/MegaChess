import sys
import traceback
import Chess
import socket
import threading

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client_start()
        self.is_game_now = False
        self.potok_start = False
        self.game_list = []
        if True:
            self.startui()
        else:
            uic.loadUi('login.ui', self)

    def startui(self):
        uic.loadUi('start.ui', self)
        self.mkgame.clicked.connect(self.create_game_start)
        self.cnktgame.clicked.connect(self.start_connect)

    def start_connect(self):
        uic.loadUi('gameslist.ui', self)
        self.backbtn.clicked.connect(self.startui)
        self.sor.sendto(f"#l".encode('utf-8'), self.server)

    def view_game_list(self):
        gml = self.game_list
        for g in gml:
            if g[1] == "public":
                self.gmwlist.addItem(g[0] + ' ✔')
            else:
                self.gmwlist.addItem(g[0] + ' ❌')

        self.gmwlist.itemDoubleClicked.connect(self.choice_game)


    def choice_game(self):
        pass

    def create_game_start(self):
        uic.loadUi('creategame.ui', self)
        self.mkbtn.clicked.connect(self.create_game)
        self.backbtn.clicked.connect(self.startui)
        self.b1.toggled.connect(lambda: self.gpEdit.setEnabled(False))
        self.b2.toggled.connect(lambda: self.gpEdit.setEnabled(True))

    def create_game(self):
        # "#n<name>=<count>=<game type>=<password if need>"
        if self.b1.isChecked():
            game_type = "public"
            self.sor.sendto(f"#n{self.name}={self.count}={game_type}".encode('utf-8'), self.server)
        else:
            game_type = "password"
            pswd = self.gpEdit.text()
            self.sor.sendto(f"#n{self.name}={self.count}={game_type}={pswd}".encode('utf-8'), self.server)

    def start_game(self):
        uic.loadUi('designe.ui', self)
        self.boardw = 800
        self.boardh = 800
        self.cagesize = 100
        self.widget.mouseReleaseEvent = self.board_click

        self.board = Chess.getBoard()
        self.taken_piece = None
        self.is_white = True

        self.pushButton.clicked.connect(self.on_click)
        self.pushButton_2.clicked.connect(self.on_click2)
        self.radioButton.setChecked(True)

    def client_start(self):
        self.name = "sasha"
        self.count = 11
        self.stip = "127.0.0.1"
        self.server = self.stip, 5059  # Данные сервера
        self.sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sor.bind(('', 0))  # Задаем сокет как клиент
        self.sor.sendto((self.name + ' Connect to server').encode('utf-8'),
                        self.server)  # Уведомляем сервер о подключении
        self.potok = threading.Thread(target=self.read_sok)
        self.potok.start()
        print("start")

    def on_click2(self):
        text = self.lineEdit_3.text()
        text = f'<div style="color: green">[{self.name}]</div> ' + text
        self.textBrowser.append(text)
        self.lineEdit_3.clear()
        self.sor.sendto(f"#@{text}".encode('utf-8'),
                        self.server)

    def paintEvent(self, event):
        if self.is_game_now:
            qp = QPainter()
            qp.begin(self)
            self.drawText(event, qp)
            qp.end()

    def drawText(self, event, qp):
        qp.drawPixmap(20, 20, 800, 800, QtGui.QPixmap("182869_after.jpeg"))
        for i in range(8):
            for j in range(8):
                if str(self.board[i][j]) == "no_piece":
                    continue
                else:
                    if self.board[i][j].is_alive:
                        qp.drawPixmap(20 + 100 * i, 20 + 100 * j, 100, 100,
                                      QtGui.QPixmap(f"assets/images/{self.board[i][j].img}.png"))
        if self.taken_piece is not None:
            qp.drawPixmap(20 + 100 * self.taken_piece[0], 20 + 100 * self.taken_piece[1], 100, 100,
                          QtGui.QPixmap(f"assets/taken.png"))

    def pmove(self, lx, ly, x, y):
        self.board[lx][ly].x = x
        self.board[lx][ly].y = y
        self.board[x][y] = self.board[lx][ly]
        self.board[lx][ly] = Chess.Spase()
        self.repaint()

    def board_click(self, e):
        # print("clicked!!")
        col = e.x() // self.cagesize
        row = (e.y() // self.cagesize)
        # print(8 - (e.y() // self.cagesize), chr((e.x() // self.cagesize) + ord("A")))

        if self.taken_piece is None:
            if str(self.board[col][row]) != "no_piece":
                if self.board[col][row].color == self.is_white:
                    self.taken_piece = (col, row)
        else:
            if self.potok_start:
                self.board[self.taken_piece[0]][self.taken_piece[1]].go(col, row, self.board)

            if str(self.board[col][row]) == "no_piece":
                self.sor.sendto(f"##{self.taken_piece[0]}={self.taken_piece[1]}={col}={row}".encode('utf-8'),
                                self.server)
                self.board[self.taken_piece[0]][self.taken_piece[1]].x = col
                self.board[self.taken_piece[0]][self.taken_piece[1]].y = row
                self.board[col][row] = self.board[self.taken_piece[0]][self.taken_piece[1]]
                self.board[self.taken_piece[0]][self.taken_piece[1]] = Chess.Spase()
                self.taken_piece = None
            else:
                if self.board[col][row].color == self.is_white:
                    self.taken_piece = (col, row)
                else:
                    self.sor.sendto(f"##{self.taken_piece[0]}={self.taken_piece[1]}={col}={row}".encode('utf-8'),
                                    self.server)

                    self.board[self.taken_piece[0]][self.taken_piece[1]].x = col
                    self.board[self.taken_piece[0]][self.taken_piece[1]].y = row
                    self.board[col][row] = self.board[self.taken_piece[0]][self.taken_piece[1]]
                    self.board[self.taken_piece[0]][self.taken_piece[1]] = Chess.Spase()
                    self.taken_piece = None

        mensahe = f"<{col} and {row}>"
        # self.sor.sendto(('[' + self.name + ']' + mensahe).encode('utf-8'), self.server)

        print(col, row)
        self.repaint()

    def read_sok(self):
        while True:
            data = self.sor.recv(1024)
            dtstr = data.decode('utf-8')
            if dtstr[:2] == "##":
                dt = list(map(int, dtstr[2:].split('=')))
                ex.pmove(dt[0], dt[1], dt[2], dt[3])
            elif dtstr[:2] == "#@":
                self.textBrowser.append(dtstr[2:])
            elif dtstr[:2] == "#l":
                gml = list(map(lambda n: n.split('&'), dtstr[2:].split('=')))
                self.game_list = gml
                self.view_game_list()



def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ex = QDialog()
    ex.show()
    # server = '127.0.0.1', 5059  # Данные сервера
    # sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sor.bind(('', 0))  # Задаем сокет как клиент
    # sor.sendto((alias + ' Connect to server').encode('utf-8'), server)  # Уведомляем сервер о подключении
    # potok = threading.Thread(target=read_sok)
    # # potok.start()
    # # print("start")
    sys.exit(app.exec_())

# 37.140.199.45
