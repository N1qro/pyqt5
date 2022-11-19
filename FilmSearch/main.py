import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic


class Window(QWidget):
    categories = {
        'Год выпуска': ('year', int),
        'Название': ('title', str),
        'Продолжительность': ('duration', int)
    }

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.searchButton.clicked.connect(self.onSearch)
        self.errorLabel.hide()

    @staticmethod
    def filterQuery(f):
        def wrapper(self, *args, **kwargs):
            queryValue = self.queryValue.text()
            queryField, queryType = self.categories[self.queryField.currentText()]
            
            try:
                assert len(queryValue) > 0
                queryValue = queryType(queryValue)
            except TypeError:
                self.errorLabel.show()
                self.errorLabel.setText('Неправильный тип данных в запросе.')
            except AssertionError:
                self.errorLabel.show()
                self.errorLabel.setText('Запрос не может быть пустым.')
            else:
                self.errorLabel.hide()
                self.errorLabel.setText('')
                f(self, queryValue, queryField)
        return wrapper

    @filterQuery
    def onSearch(self, queryValue, queryField):
        query = f"""
            SELECT films.id, films.title, year, genres.title, duration
            FROM films
            JOIN genres ON films.genre == genres.id
            WHERE films.{queryField} = (?)
            ORDER BY films.id ASC
        """

        db = sqlite3.connect('films_db.sqlite')
        cursor = db.cursor()
        data = cursor.execute(query, (queryValue,)).fetchone()

        if data is None:
            self.id.setText('')
            self.name.setText('')
            self.releaseYear.setText('')
            self.genre.setText('')
            self.duration.setText('')
            return self.errorLabel.setText('Не было найдено ни одного фильма.')

        self.id.setText(str(data[0]))
        self.name.setText(data[1])
        self.releaseYear.setText(str(data[2]))
        self.genre.setText(data[3].capitalize())
        self.duration.setText(str(data[4]))





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
