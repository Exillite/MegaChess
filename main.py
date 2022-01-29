import sys
import traceback
import Chess

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('designe.ui', self)
        self.boardw = 800
        self.boardh = 800
        self.cagesize = 100
        self.widget.mouseReleaseEvent = self.board_click

        self.board = Chess.getBoard()
        self.taken_piece = None

    def paintEvent(self, event):
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
                    qp.drawPixmap(20 + 100 * i, 20 + 100 * j, 100, 100, QtGui.QPixmap(f"assets/images/{self.board[i][j].img}.png"))
        if self.taken_piece is not None:
            qp.drawPixmap(20 + 100 * self.taken_piece[0], 20 + 100 * self.taken_piece[1], 100, 100, QtGui.QPixmap(f"assets/taken.png"))

    def board_click(self, e):
        # print("clicked!!")
        col = e.x() // self.cagesize
        row = (e.y() // self.cagesize)
        # print(8 - (e.y() // self.cagesize), chr((e.x() // self.cagesize) + ord("A")))

        if self.taken_piece is None:
            if str(self.board[col][row]) != "no_piece":
                self.taken_piece = (col, row)
        else:
            self.board[self.taken_piece[0]][self.taken_piece[1]].go(col, row, self.board)

            if str(self.board[col][row]) == "no_piece":
                self.board[self.taken_piece[0]][self.taken_piece[1]].x = col
                self.board[self.taken_piece[0]][self.taken_piece[1]].y = row
                self.board[col][row] = self.board[self.taken_piece[0]][self.taken_piece[1]]
                self.board[self.taken_piece[0]][self.taken_piece[1]] = Chess.Spase()
                self.taken_piece = None
            else:
                self.taken_piece = (col, row)



        print(col, row)
        self.repaint()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ex = QDialog()
    ex.show()
    sys.exit(app.exec_())
