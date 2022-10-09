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

        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        if not self.fname:
            sys.exit(0)
        self.openImage(self.fname)

        self.channels.buttonClicked.connect(self.onChannelClick)
        self.rotations.buttonClicked.connect(self.onRotate)

    def onRotate(self, btn) -> None:
        angle = -90 if btn.objectName()[-1] == 'R' else 90
        self.im = Image.open('temp.png' if os.path.exists('temp.png') else self.fname)
        out = self.im.rotate(angle)
        out.save('temp.png')
        self.openImage('temp.png')


    def onChannelClick(self, btn) -> None:
        self.im = Image.open(self.fname)
        self.pixels = self.im.load()
        self.x, self.y = self.im.size

        func = self.funcs[btn.text()]
        self.pixels = list(map(func, self.im.getdata()))
        self.im.putdata(self.pixels)

        self.im.save('temp.png')
        self.openImage('temp.png')

    def openImage(self, fname) -> None:
        self.pixmapI = QPixmap(fname)
        self.output.setPixmap(self.pixmapI)
        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PILWindow()
    window.show()
    
    err = app.exec_()
    os.remove('temp.png')
    sys.exit(err)
