import sys

from PyQt5 import uic
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setFixedSize(self.size())
        self.submitButton.clicked.connect(self.onSubmit)
        self.toDraw = None

    def getInputs(self) -> tuple:
        sideLen = self.sideLen.value()
        multiplier = self.multiplier.value()
        amount = self.amount.value()

        return sideLen, multiplier, amount

    def paintEvent(self, event) -> None:
        qp = QPainter()
        qp.begin(self)
        if self.toDraw:
            self.drawSquares(qp)
        qp.end()

    def drawSquares(self, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(100, 100, 100))
        qp.drawRects(*self.toDraw)

    def onSubmit(self) -> None:
        center = self.canvas.frameGeometry().center()
        side, mul, n = self.getInputs()

        squares = list()
        for i in range(n):
            side = round(side * mul ** i)
            square = QRect(0, 0, side, side)
            square.moveCenter(center)
            squares.append(square)

        self.toDraw = squares
        # print(squares)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
