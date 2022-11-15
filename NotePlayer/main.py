import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtMultimedia
from PyQt5 import uic


class NoteWindow(QWidget):
    codes = {
        QtCore.Qt.Key.Key_Q: 'do',
        QtCore.Qt.Key.Key_W: 're',
        QtCore.Qt.Key.Key_E: 'mi',
        QtCore.Qt.Key.Key_R: 'fa',
        QtCore.Qt.Key.Key_T: 'soli',
        QtCore.Qt.Key.Key_Y: 'lya',
        QtCore.Qt.Key.Key_U: 'si'
    }

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadMp3s()
        self.notes.buttonClicked.connect(self.onButtonClick)

    def onButtonClick(self, btn):
        keyId = getattr(QtCore.Qt.Key, 'Key_' + btn.text())
        self.codes[keyId].play()

    def loadMp3s(self):
        for keyId, filename in self.codes.items():
            media = QtCore.QUrl.fromLocalFile(filename + '.mp3')
            content = QtMultimedia.QMediaContent(media)
            self.codes[keyId] = QtMultimedia.QMediaPlayer()
            self.codes[keyId].setMedia(content)

    def keyPressEvent(self, event) -> None:
        keyId = event.key()
        if keyId in self.codes:
            self.codes[keyId].play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NoteWindow()
    window.show()
    sys.exit(app.exec_())
