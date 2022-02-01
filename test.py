import sys
import traceback

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class QDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        if 1 < 2:
            uic.loadUi('start.ui', self)
        self.mkgame.clicked.connect(self.f)

    def f(self):
        uic.loadUi('reg.ui', self)


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ex = QDialog()
    ex.show()
    sys.exit(app.exec_())
