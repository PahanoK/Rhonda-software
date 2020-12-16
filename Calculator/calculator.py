import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import calculator_ui
from functools import partial

class CalculatorApp(QtWidgets.QMainWindow, calculator_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.inputNumber = "0"
        self.storedNumber = "0"
        self.displayNumber = float(self.inputNumber)
        self.lcdNumber.display(self.displayNumber)
        self.state = ""
        self.storedState = ""
        self.actions = ["plus", "minus", "multi", "division"]

        for i in range(10):
            button = getattr(self, 'n%s' % i)
            button.clicked.connect(partial(self.number, i))

        self.cancelEntry.clicked.connect(self.p_cancel)
        self.clear.clicked.connect(self.p_clear)
        self.equal.clicked.connect(self.p_equal)
        self.dot.clicked.connect(self.p_dot)

        for i in self.actions:
            button = getattr(self, i)
            button.clicked.connect(partial(self.set_action, i))

    def lcd_update(self):
        self.displayNumber = float(self.inputNumber)
        self.lcdNumber.display(self.displayNumber)

    def p_dot(self):
        if "." not in self.inputNumber:
            self.inputNumber += "."
        self.lcd_update()

    def p_clear(self):
        self.state = ""
        self.storedState = ""
        self.inputNumber = "0"
        self.storedNumber = "0"
        self.lcd_update()

    def p_cancel(self):
        self.inputNumber = "0"
        if self.storedState == "minus":
            self.inputNumber = "-0"
        self.lcd_update()

    def store_number(self):
        self.storedNumber = self.inputNumber
        self.inputNumber = "0"

    def set_action(self, action):
        if self.storedState != "" and self.state != "equal":
            self.p_equal()
        self.store_number()
        self.state = action

    def p_equal(self):
        if self.storedState == "plus" or self.storedState == "minus":
            if self.state != "equal":
                self.inputNumber, self.storedNumber = self.storedNumber, self.inputNumber
            self.inputNumber = str(float(self.inputNumber) + float(self.storedNumber))

        if self.storedState == "multi":
            if self.state != "equal":
                self.inputNumber, self.storedNumber = self.storedNumber, self.inputNumber
            self.inputNumber = str(float(self.inputNumber) * float(self.storedNumber))

        if self.storedState == "division" and float(self.inputNumber) != 0:
            if self.state != "equal":
                self.inputNumber, self.storedNumber = self.storedNumber, self.inputNumber
            self.inputNumber = str(float(self.inputNumber) / float(self.storedNumber))

        self.state = "equal"
        self.lcd_update()

    def number(self, n):
        if self.state != "":
            self.storedState = self.state
            self.inputNumber = "0"
            if self.storedState == "minus":
                self.inputNumber = "-"
            self.state = ""
        self.inputNumber += str(n)
        self.lcd_update()


    def key_press_event(self, event):
        for i in range(10):
            if event.key() == getattr(QtCore.Qt, 'Key_%s' % i):
                self.number(i)
        if event.key() == QtCore.Qt.Key_Plus:
            self.set_action("plus")
        if event.key() == QtCore.Qt.Key_Minus:
            self.set_action("minus")
        if event.key() == QtCore.Qt.Key_Asterisk:
            self.set_action("multi")
        if event.key() == QtCore.Qt.Key_division:
            self.set_action("division")
        if event.key() == QtCore.Qt.Key_Equal:
            self.p_equal()
        if event.key() == QtCore.Qt.Key_Enter:
            self.p_equal()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = CalculatorApp()
    window.setObjectName("Calculator")
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()