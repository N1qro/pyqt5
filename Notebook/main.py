import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout


def layout_widgets(layout):
    return (layout.itemAt(i) for i in range(layout.count()))


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.submitBtn.clicked.connect(self.onClick)

    def onClick(self):
        name = self.nameEdit.text()
        number = self.numberEdit.text()
        if name.isalpha() and number.isdecimal():
            self.listOutput.addItem(f'{name}: {number}')
        else:
            print('Неправильно заполнены поля.')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
