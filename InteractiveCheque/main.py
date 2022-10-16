import sys
import csv

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5 import uic


class ChequeWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.prices = dict.fromkeys(range(self.table.rowCount()), 0)

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
                    self.table.setItem(i, j, QTableWidgetItem(elem))

        self.table.cellChanged.connect(self.onCountChange)
        self.adjustSize()
        self.setFixedSize(self.size())
    
    def onCountChange(self, row, column):
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
