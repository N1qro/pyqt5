import random
import sys
import string

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5 import uic


def showMessage(text):
    msg = QMessageBox()
    msg.setWindowTitle('Уведомление')
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.exec_()


class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.setButton.clicked.connect(self.onSet)
        self.clearButton.clicked.connect(self.graphicsView.clear)

    def inputChecker(f):
        def wrapper(self):
            formula = self.fInput.text().lower().replace(
                ' ', '').replace('^', '**').replace(':', '/')
            startPoint = self.fromInput.value()
            endPoint = self.toInput.value()

            hasNoOtherLetters = True
            for sym in formula:
                if sym in string.ascii_lowercase.replace('x', '').replace('y', ''):
                    hasNoOtherLetters = False
                    break
            try:
                assert formula[0] == 'y', 'Формула без зависимости'
                assert formula[1] == '=', 'Несокращенные формулы не принимаются'
                assert hasNoOtherLetters, 'В уравнении могут использоваться только X и Y'
                assert startPoint < endPoint, 'Задан неправильный диапазон'

                xS = list(range(startPoint, endPoint))
                yS = [eval(formula[2:]) for x in xS]
            except AssertionError as e:
                showMessage(str(e))
            except ZeroDivisionError:
                showMessage('В заданном диапазоне формуле где-то делит на 0!')
            except SyntaxError:
                showMessage('Знаки расставлены в странном порядке или их нет.')
            except Exception as e:
                showMessage(
                    'Возникла непредвиденная ошибка. Исправьте формулу')
            else:
                f(self, xS, yS)
        return wrapper

    @inputChecker
    def onSet(self, xS, yS):
        self.graphicsView.clear()
        self.graphicsView.plot(xS, yS)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    window.onSet()
    sys.exit(app.exec_())
