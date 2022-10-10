import sys
import os

from typing import TextIO
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic


class MixWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('main.ui', self)
        self.file = self.findAppropriateFile()
        self.submitButton.clicked.connect(self.onClick)

    def findAppropriateFile(self) -> TextIO:
        for file in os.listdir("."):
            if file.endswith(".txt"):
                return os.path.join(".", file)
        else:
            self.submitButton.setDisabled(True)
            self.submitButton.setText('В директории нет никакого текстового файла.')

    def onClick(self) -> None:
        with open(self.file, encoding='UTF-8') as f:
            lines = list(map(str.strip, f.readlines()))
            self.output.setPlainText('\n'.join(lines[1::2]))
            self.output.appendPlainText('\n'.join(lines[::2]))
            self.submitButton.setDisabled(True)
            self.submitButton.setText(f'Строки из "{self.file[2:]}" были успешно загружены.')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MixWindow()
    window.show()
    sys.exit(app.exec_())
