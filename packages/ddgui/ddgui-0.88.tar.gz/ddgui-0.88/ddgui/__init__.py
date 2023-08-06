import sys
import time
import itertools # for the zip()

from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThreadPool, QRunnable, QThread

from PyQt5 import QtWidgets, uic
import sys

def tambah_angka(a,b):
    return a+b

def kali_angka(a,b):
    return a*b

def bagi_angka(a,b):
    return a/b

def kurang_angka(a,b):
    return a-b

def ddprint(a):
    return a

#input("DD GUI Library has been installed.")



# First Method

"""

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

"""

#Second Method
#app = QApplication(sys.argv)
#window = QWidget()
#window.show()
#sys.exit(app.exec())



# Third Method

class Ui(QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ddgui.ui', self)

        self.pushButtonExit.clicked.connect(self.exitMethod)
        self.show()

        #self.button = self.findChild(QtWidgets.QPushButton, 'printButton') # Find the button
        #self.button.clicked.connect(self.printButtonPressed) # Remember to pass the definition/method, not the return value!
        #self.input = self.findChild(QtWidgets.QLineEdit, 'input')

    def exitMethod(self):
        QApplication.instance().quit()

    #def printButtonPressed(self):
    #    # This is executed when the button is pressed
    #    print('Input text:' + self.input.text())

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()


# Forth Method

"""
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ddgui.ui', self)
        self.show()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

"""




