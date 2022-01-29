import sys
import traceback
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


        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.drawPixmap(20, 20, 800, 800, QtGui.QPixmap("182869_after.jpeg"))
        for i in range(8):
            qp.drawPixmap(20 + 100 * i, 120, 100, 100, QtGui.QPixmap("assets/images/wp.png"))

    def board_click(self, e):
        # print("clicked!!")
        self.repaint()
        col = e.x() // self.cagesize
        row = 8 - (e.y() // self.cagesize)
        print(8 - (e.y() // self.cagesize), chr((e.x() // self.cagesize) + ord("A")))


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ex = QDialog()
    ex.show()
    sys.exit(app.exec_())
