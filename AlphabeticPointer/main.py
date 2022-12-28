import sys
import sqlite3
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QButtonGroup, QTableView, QVBoxLayout, QHBoxLayout
from PyQt5 import uic   

alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)

        with sqlite3.connect('films_db.sqlite') as con:
            amount = len(con.cursor().execute('SELECT * FROM films').fetchall())

        self.statusBar.showMessage(f'Найдёно {amount} строк данных')
        self.alphabetLayout.setLayout(QHBoxLayout())
        self.tableViewWidget.setLayout(QVBoxLayout())

        self.alphabetButtons = QButtonGroup(self)
        for letter in alphabet:
            btn = QPushButton(letter, self.alphabetLayout)
            btn.setFixedSize(25, 25)
            self.alphabetLayout.layout().addWidget(btn)
            self.alphabetButtons.addButton(btn)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('films_db.sqlite')
        self.db.open()

        self.view = QTableView(self.tableViewWidget)
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('films')
        self.model.select()

        self.view.setModel(self.model)
        self.view.move(10, 10)
        self.view.resize(617, 315)
        self.view.hideColumn(0)

        self.tableViewWidget.layout().addWidget(self.view)
        self.alphabetButtons.buttonClicked.connect(self.filterEntries)

    def filterEntries(self, btn):
        self.model.setFilter(f'title LIKE "{btn.text()}%"')

        # Получаем количество 
        with sqlite3.connect('films_db.sqlite') as con:
            lst = con.cursor().execute(f'SELECT * FROM films WHERE title LIKE "{btn.text()}%"').fetchall()

        self.statusBar.showMessage(f"Найдёно {len(lst)} строк данных")

    def loadTable(self):
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


