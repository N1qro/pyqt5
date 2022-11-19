import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.searchButton.clicked.connect(self.onSearch)
        self.loadCheckboxes()

    def loadCheckboxes(self):
        db = sqlite3.connect('films_db.sqlite')
        cursor = db.cursor()

        genres = cursor.execute('SELECT title FROM genres').fetchall()
        self.genreChooser.addItems(genre[0].capitalize() for genre in genres)

    def onSearch(self):
        db = sqlite3.connect('films_db.sqlite')
        cursor = db.cursor()

        query = f"""
            SELECT films.title, genres.title, year
            FROM films
            JOIN genres ON films.genre == genres.id
            WHERE genres.title = (?)
            ORDER BY films.id ASC
        """

        data = cursor.execute(
            query, (self.genreChooser.currentText().lower(),)).fetchall()  # fetchmany(100)

        title = ['Название', 'Жанр', 'Год']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
