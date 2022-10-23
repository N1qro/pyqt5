import sys
import sqlite3

from os.path import join
from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


class Popup(QWidget):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('popup.ui', self)



class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('main.ui', self)
        self.dbCursor = sqlite3.connect('MyDB.db').cursor()
        self.submitButton.clicked.connect(self.onSubmit)
        self.query = """
            SELECT * 
            FROM Library 
        """

    def onSubmit(self) -> None:
        category = self.searchBy.currentText()
        expression = self.searchParams.text()

        query = self.query
        if expression:
            query += f'WHERE {category} LIKE "%{expression}%"'

        data = self.dbCursor.execute(query)
        for id_, name, author, year, genre, preview in data:
            btn = QPushButton(name, self)

            clickFunc = partial(self.displayInfo, name,
                                author, year, genre, preview)
            btn.clicked.connect(clickFunc)

            item = QListWidgetItem()
            item.setSizeHint(btn.sizeHint())
            self.displayList.addItem(item)
            self.displayList.setItemWidget(item, btn)

    def displayInfo(self, name, author, year, genre, preview) -> None:
        self.popup = Popup()
        if preview:
            print(preview)
            pixmap = QPixmap(join('bookCovers', preview))
        else:
            pixmap = QPixmap(join('bookCovers', 'default.png'))
        self.popup.preview.setPixmap(pixmap)
        self.popup.bookAuthor.setText(author)
        self.popup.bookTitle.setText(name)
        self.popup.bookGenre.setText(genre)
        self.popup.bookReleaseYear.setText(str(year))

        self.popup.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
