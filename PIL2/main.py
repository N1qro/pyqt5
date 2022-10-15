import sys
import os
from PIL import Image
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


class PILWindow(QMainWindow):
    funcs = {
        'R': lambda clr: (clr[0], 0, 0),
        'G': lambda clr: (0, clr[1], 0),
        'B': lambda clr: (0, 0, clr[2]),
        'ALL': lambda clr: clr
    }

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('main.ui', self)
        self.channels.buttonClicked.connect(self.onChannelSwitch)
        self.rotations.buttonClicked.connect(self.onRotate)
        self.getImageData()

    def onChannelSwitch(self, btn):
        channel = btn.text()
        self.image.putdata(list(map(self.funcs[channel], self.defaultImage.getdata())))
        self.image.rotate(self.rotationAngle).save('temp.jpg')
        self.openImageInPixmap()

    def onRotate(self, btn):
        self.rotationAngle += -90 if btn.objectName()[-1] == 'R' else 90
        
        self.image.rotate(self.rotationAngle).save('temp.jpg')
        self.openImageInPixmap()

    def getImageData(self):
        filename = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '', 'Картинка (*.jpg);;Картинка (*.jpeg)')[0]

        self.openImageInPixmap(fname=filename)
        self.defaultImage = Image.open(filename)
        self.image = Image.open(filename)
        self.rotationAngle = 0

    def openImageInPixmap(self, fname='temp.jpg') -> None:
        self.pixmapI = QPixmap(fname)
        self.output.setPixmap(self.pixmapI)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PILWindow()
    window.show()

    err = app.exec_()
    if os.path.exists('temp.jpg'):
        os.remove('temp.jpg')
    sys.exit(err)
