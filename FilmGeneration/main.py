import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QMessageBox
from PyQt5 import uic


def show_popup(win, entry_id):
    msg = QMessageBox(win)
    msg.setWindowTitle("Подтверждение")
    msg.setText(f"Уверены что хотите заменить запись с id={entry_id}?")
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
    result = msg.exec_()
    return result


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.db = sqlite3.connect('films_db.sqlite')
        # self.db.create_function('REVSTR', 1, lambda s: s[::-1])
        self.currentId = None

        uic.loadUi('main.ui', self)
        self.launchButton.clicked.connect(self.loadEntry)
        self.updateButton.clicked.connect(self.updateEntry)

    def updateEntry(self):
        if self.currentId == None:
            self.loadEntry()

        if show_popup(self, self.currentId) == QMessageBox.Ok:
            row = list(self.db.cursor().execute("""
                SELECT * FROM films
                WHERE id = (?)
            """, (str(self.currentId),)).fetchone())

            self.db.cursor().execute("""
                DELETE FROM films
                WHERE id = ?
            """, (self.currentId,))

            row[1] = row[1][::-1]
            row[2] = row[2] + 1000
            row[-1] = row[-1] * 2

            self.db.cursor().execute("""
                INSERT INTO films
                VALUES (?, ?, ?, ?, ?)
            """, row)

            self.db.commit()
            self.loadEntry()

    def loadEntry(self):
        entry_id = self.idBox.value()

        cursor = self.db.cursor()
        data = cursor.execute("""
            SELECT * FROM films
            WHERE id = (?)
        """, (str(entry_id),)).fetchone()

        headers = [item[0] for item in cursor.description]

        if data:
            self.tableWidget.setColumnCount(len(headers))
            self.tableWidget.setHorizontalHeaderLabels(headers)
            self.tableWidget.setRowCount(1)

            for j, elem in enumerate(data):
                self.tableWidget.setItem(
                    0, j, QTableWidgetItem(str(elem)))

            self.currentId = entry_id
            self.tableWidget.resizeColumnsToContents()
        else:
            self.tableWidget.clear()
            self.currentId = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    err = app.exec_()
    window.db.close()
    sys.exit(err)
