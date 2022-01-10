from distutils.util import strtobool
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QCheckBox
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget, QLineEdit
import sys

class Main(QMainWindow):

    def __init__(self):
        super().__init__()


def main():
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
