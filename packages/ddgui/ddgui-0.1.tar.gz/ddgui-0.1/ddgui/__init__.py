import sys
import time
import itertools # for the zip()

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThreadPool, QRunnable, QThread

class MyForm(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = loadUi("ddgui.ui", self)
        self.ui.pushButtonExit.clicked.connect(self.exitMethod)
        self.show()

    def exitMethod(self):
        QApplication.instance().quit()

if __name__ == "__main__":
    a = QApplication(sys.argv)
    form = MyForm()
    form.show()
    a.exec_()