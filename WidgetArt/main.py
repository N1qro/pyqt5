import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QFont

testExample = [
    [1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1]
]


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.main()

    def main(self):
        for i, row in enumerate(testExample):
            for j, elem in enumerate(row):
                newButton = QPushButton(str(elem), self)
                newButton.setFont(QFont("Times", 15))
                newButton.setMinimumSize(50, 50)
                newButton.setMaximumSize(50, 50)
                newButton.setStyleSheet(
                    f'QPushButton {{background-color: {"#30c557" if elem else "#e71d1d"}}}')
                self.gridLayout.addWidget(newButton, i, j)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
