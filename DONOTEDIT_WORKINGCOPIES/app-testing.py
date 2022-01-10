import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp
from PyQt5.QtCore import Qt, QEvent, QObject
from ui_main import Ui_MainWindow


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        qApp.installEventFilter(self)
        self.pushButton.clicked.connect(self.clickButton()) #here is where the issue is occurs
        self.show()
        self.setupUi(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.close()
        return super(MyMainWindow, self).eventFilter(obj, event)

    def clickButton(self):
        sender = self.sender()
        self.statusbar().showMessage(sender.text() + ' was pressed')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyMainWindow()
    test = TestClass()
    sys.exit(app.exec_())