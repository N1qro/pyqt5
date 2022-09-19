import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout

def layout_widgets(layout):
   return (layout.itemAt(i) for i in range(layout.count()))

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.groups = [self.firstColor, self.secondColor, self.thirdColor]
        self.submitBtn.clicked.connect(self.onClick)

    def onClick(self):
        colors = [group.checkedButton().text() for group in self.groups]
        self.displayInfo.setText('Цвета: {}, {} и {}'.format(*colors))


        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())