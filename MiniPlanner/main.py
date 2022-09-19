import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.submitButton.clicked.connect(self.onClick)

    def onClick(self):
        today = self.calendarWidget.selectedDate().getDate()
        dateStr = '-'.join(map(str, today))
        time = self.timeEdit.time().toString()
        toDo = self.lineEdit.text()
        if toDo:
            dateTime = f'{dateStr} {time} - {toDo}'
            self.listWidget.addItem(dateTime)
        else:
            print('Поле не заполнено!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
