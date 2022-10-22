import random
import sys

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget


class Window(QWidget):
    availableColors = ('red', 'orange', 'green', 'blue', 'pink', 'yellow')

    def __init__(self) -> None:
        super().__init__()
        self.pixmaps = self.getPixmaps()
        self.chosenCar = 'pink'
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self) -> None:
        self.setWindowTitle('Машинка')
        self.resize(400, 400)

        self.label = QLabel(self)
        self.label.resize(60, 30)
        self.label.setScaledContents(True)
        self.loadPixmap()

    def mouseMoveEvent(self, event) -> None:
        x, y = event.x(), event.y()
        frame = self.label.geometry()
        frame.moveCenter(QPoint(x, y))

        if frame.x() < 0:
            return
        elif frame.x() > self.width() - self.label.width():
            return
        elif frame.y() < 0:
            return
        elif frame.y() > self.height() - self.label.height():
            return

        self.label.move(frame.topLeft())

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Space:
            self.loadPixmap()

    def getPixmaps(self) -> dict:
        pixmaps = dict()
        for name in self.availableColors:
            pixmaps[name] = QPixmap(name + '.png').scaled(60, 30)
        return pixmaps

    def loadPixmap(self) -> None:
        color = random.choice(self.availableColors)
        while color == self.chosenCar:
            color = random.coice(self.availableColors)
        self.chosenCar = color

        self.label.setPixmap(self.pixmaps[color])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
