import sys
import csv

from random import randint
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QVariant
from PyQt5 import uic


class ChequeWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.prices = dict.fromkeys(range(self.table.rowCount()), 0)
        self.reColoring = False

        self.updateButton.clicked.connect(self.onReColor)
        self.table.cellChanged.connect(self.onCountChange)

    def initUI(self) -> None:
        uic.loadUi('main.ui', self)

        with open('price.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            title = next(reader) + ['Количество']
            self.table.setColumnCount(len(title))
            self.table.setHorizontalHeaderLabels(title)
            self.table.setRowCount(0)

            for i, row in enumerate(reader):
                self.table.setRowCount(self.table.rowCount() + 1)
                for j, elem in enumerate(row + ['0']):
                    it = QTableWidgetItem()
                    it.setData(Qt.EditRole, QVariant(int(elem) if elem.isdigit() else elem))
                    if j in (0, 1):
                        it.setFlags(Qt.ItemIsEnabled)

                    # if elem.isdigit():
                    #     # Я потратил 2 часа своего времени, чтобы найти
                    #     # эту сраную строчку
                    #     it.setData(Qt.EditRole, QVariant(int(elem)))
                    # else:
                    #     it.setText(elem)

                    self.table.setItem(i, j, it)

        self.sortItemsByPrice()
        self.adjustSize()
        self.setFixedSize(self.size())

    def reColorWholeRow(self, row, color) -> None:
        for i in range(self.table.columnCount()):
            self.table.item(row, i).setBackground(color)

    def getRandomColor(self) -> None:
        return QColor(randint(0, 255), randint(0, 255), randint(0, 255))

    def onReColor(self) -> None:
        self.reColoring = True
        for row, color in enumerate([self.getRandomColor() for _ in range(5)]):
            self.reColorWholeRow(row, color)
        self.reColoring = False

    def sortItemsByPrice(self) -> None:
        self.table.setSortingEnabled(True)
        self.table.sortItems(1, Qt.DescendingOrder)

    def onCountChange(self, row, column):
        if self.reColoring:
            return

        priceBefore = self.prices[row]
        price = int(self.table.item(row, 1).text())
        count = int(self.table.item(row, column).text())

        if count < 0:
            self.table.item(row, column).setText('0')
        else:
            priceNow = price * count
            self.prices[row] = priceNow
            self.output.setText(str(sum(self.prices.values())))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChequeWindow()
    window.show()
    sys.exit(app.exec_())
