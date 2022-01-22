import sys
import traceback
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class QDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('designe.ui', self)
        self.boardw = 800
        self.boardh = 800
        self.cagesize = 100
        self.widget.setStyleSheet("background-image : url(182869_after.jpeg)")
        self.widget.mouseReleaseEvent = self.board_click

    def board_click(self, e):
        print("clicked!!")
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
