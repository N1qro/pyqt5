import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

MOVESPEED = 10


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()

        self.UFO_MOVE_TABLE = {
            87: lambda: self.UFOMoveRel(0, -MOVESPEED),
            65: lambda: self.UFOMoveRel(-MOVESPEED, 0),
            83: lambda: self.UFOMoveRel(0, MOVESPEED),
            68: lambda: self.UFOMoveRel(MOVESPEED, 0)
        }

    def UFOMoveRel(self, xVal=0, yVal=0):
        previous = self.label.pos()
        previous.setX(previous.x() + xVal)
        previous.setY(previous.y() + yVal)

        qRect = self.label.geometry()
        qRect.moveCenter(previous)

        self.label.move(previous)
        newX, newY = self.label.pos().x(), self.label.pos().y()

        if newX < 0:
            self.label.move(self.width() - self.label.width(), newY)
        elif newX > self.width() - self.label.width():
            self.label.move(0, newY)
        elif newY < 0:
            self.label.move(newX, self.height() - self.label.height())
        elif newY > self.height() - self.label.height():
            self.label.move(newX, 0)

    def initUI(self) -> None:
        self.setWindowTitle('Управление НЛО')
        self.resize(400, 400)

        # Create a UFO and move it to Center
        pixmap = QPixmap('sprite.png')
        self.label = QLabel(self)
        self.label.resize(55, 40)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        qRect = self.label.frameGeometry()
        qRect.moveCenter(self.geometry().center())
        self.label.move(qRect.topLeft())

    def keyPressEvent(self, event) -> None:
        key = event.key()
        if key in self.UFO_MOVE_TABLE:
            self.UFO_MOVE_TABLE[key]()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
