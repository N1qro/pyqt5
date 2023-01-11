import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5 import uic


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.fill_table()
        self.tableWidget.adjustSize()
        self.lineEdit.textChanged.connect(self.on_type)
        self.filtered = False

    def on_type(self, txt):
        if len(txt) < 3 and self.filtered:
            self.fill_table()
            self.filtered = False
            return
        elif len(txt) < 3:
            return

        self.fill_table(txt)
        self.filtered = True



    def fill_table(self, filterstring=''):
        green_color = QColor(0, 255, 0)
        red_color = QColor(255, 0, 0)

        with open('titanic.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            title = next(reader)
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            i = -1
            for row in reader:
                if filterstring and filterstring.lower() not in row[1].lower():
                    continue
                i += 1
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                
                survived = False
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(elem))

                    if j == 5 and elem == '1':
                        survived = True

                self.color_row(i, green_color if survived else red_color)

        self.tableWidget.resizeColumnsToContents()

    def color_row(self, row, color):
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.item(row, i).setBackground(color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
