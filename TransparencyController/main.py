import sys

from PyQt5 import uic
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.slider.valueChanged.connect(self.onValueChanged)

    def onValueChanged(self, value):
        new_pix = QPixmap(self.defpix.size())
        new_pix.fill(Qt.transparent)
        painter = QPainter(new_pix)
        painter.setOpacity(value * 0.01)
        painter.drawPixmap(QPoint(), self.defpix)
        painter.end()
        self.picture.setPixmap(new_pix)

    def initUI(self):
        uic.loadUi('main.ui', self)
        filepath = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.defpix = QPixmap(filepath)
        self.picture.setPixmap(self.defpix)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
