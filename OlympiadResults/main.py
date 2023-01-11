import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5 import uic


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Загружаем CSV данные в программу.
        with open('rez.csv', encoding='UTF-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            next(csv_reader)
            self.data = list(csv_reader)

        uic.loadUi('main.ui', self)
        self.fill_filters()
        self.populate_table()
        self.submit_button.clicked.connect(self.on_click)

    def on_click(self):
        filters = self.get_filter_data()
        self.populate_table(filters)

    def get_filter_data(self):
        sch = self.school_filter.currentText()
        cs = self.class_filter.currentText()
        return (sch if sch != 'Все' else None, cs if cs != 'Все' else None)

    def fill_filters(self):
        all_sch = set()
        all_cls = set()
        for line in self.data:
            login = line[2]
            sch_num, cls_num = login.split('-')[2:4]
            all_sch.add(sch_num)
            all_cls.add(cls_num)

        self.school_filter.addItems(sorted(all_sch))
        self.class_filter.addItems(sorted(all_cls))

    def populate_table(self, filters=None):
        title = ('Фамилия', 'Результат')

        rows = list()
        for line in self.data:

            username = line[1]
            sch_num, cls_num, surname = username.split()[1:4]

            if filters is not None:
                if filters[0]:  # School check
                    if sch_num != filters[0]:
                        continue
                if filters[1]:  # Class check
                    if cls_num != filters[1]:
                        continue

            result = line[-1]
            rows.append((surname, result))

        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(rows):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(elem))

        self.tableWidget.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
