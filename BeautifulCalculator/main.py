import sys

from math import factorial, sqrt, floor
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('calc.ui', self)

        self.buttonGroup_digits.buttonClicked.connect(self.onDigitClick)
        self.buttonGroup_binary.buttonClicked.connect(self.onBinaryClick)
        self.btn_eq.clicked.connect(self.onEquals)
        self.btn_dot.clicked.connect(self.onDot)
        self.btn_clear.clicked.connect(self.onClear)
        self.btn_sqrt.clicked.connect(self.onSqrt)
        self.btn_fact.clicked.connect(self.onFact)

        # self.number1 = ''
        # self.number2 = ''
        # self.selectedOperation = None

        self.stack = ['', '', None]  # number1, number2, operation

    def updateLCD(self) -> None:
        self.table.display(
            self.stack[1] if self.stack[1] else self.stack[0] if self.stack[0] else '0')

    def onDigitClick(self, btn) -> None:
        self.stack[int(bool(self.stack[2]))] += btn.text()

        # if not self.self.stack[2]:
        #     self.stack[0] += btn.text()
        # else:
        #     self.stack[1] += btn.text()
        self.updateLCD()

    def onBinaryClick(self, btn) -> None:
        self.stack[2] = btn.text().replace('^', '**')

    def onEquals(self) -> None:
        print(self.stack)

        # if self.stack[1] == '0' and self.stack[2] == '/':
        #     self.table.display

        try:
            self.stack[0] = str(eval('{0} {2} {1}'.format(*self.stack)))
        except ZeroDivisionError:
            self.onClear()
            return self.table.display('Err')
        except SyntaxError:
            pass

        self.stack[1] = ''
        self.stack[2] = None
        self.updateLCD()

    def onDot(self) -> None:
        if '.' not in self.stack[int(bool(self.stack[2]))]:
            self.stack[int(bool(self.stack[2]))] += '.'

        self.updateLCD()

    def onClear(self) -> None:
        self.stack = ['', '', None]
        self.updateLCD()

    def onSqrt(self) -> None:
        self.stack[0] = str(sqrt(float(self.stack[0])))
        self.updateLCD()

    def onFact(self) -> None:
        number = float(self.stack[0])
        if floor(number) == number:
            self.stack[0] = str(factorial(floor(float(self.stack[0]))))
        else:
            print('Только целые числа могут быть факториалом!')
        self.updateLCD()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
