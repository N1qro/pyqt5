import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic


class TextEditor(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('main.ui', self)
        self.createButton.clicked.connect(self.createFile)
        self.saveButton.clicked.connect(self.saveFile)
        self.openButton.clicked.connect(self.openFile)
        self.fileNameInput.textEdited.connect(self.onEditFinish)

        self.openFileName = None

    def onEditFinish(self):
        name = self.sender().text()
        if self.openFileName and name != self.openFileName:
            self.saveButton.setEnabled(False)
        else:
            self.saveButton.setEnabled(True)

    def getName(self):
        name = self.fileNameInput.text()
        if not name:
            return None

        if not name.endswith('.txt'):
            dotIndex = name.rfind('.')
            if dotIndex != -1:
                name = name[:dotIndex] + '.txt'
            else:
                name += '.txt'

        return name

    def openFile(self):
        name = self.getName()
        try:
            with open(name, encoding='UTF-8') as f:
                self.workingOnLabel.setText(f'Открыт "{name}"')
                self.IOfield.setPlainText(f.read())
                self.IOfield.setEnabled(True)
                self.saveButton.setEnabled(True)
                self.openFileName = name
        except FileNotFoundError:
            self.IOfield.setPlainText('')
            self.IOfield.setEnabled(False)
            self.workingOnLabel.setText(f'Файл "{name}" не найден.')

    def saveFile(self):
        if not self.IOfield.isEnabled():
            return

        name = self.getName()
        text = self.IOfield.toPlainText()

        with open(name, 'w', encoding='UTF-8') as file:
            print(text, file=file)

    def createFile(self):
        name = self.getName()
        if not name:
            self.fileNameInput.setPlaceholderText('Имя файла не указано!')
            return

        self.fileNameInput.setText(name)
        self.workingOnLabel.setText(f'Открыт "{name}"')
        self.openFileName = name
        self.IOfield.setPlainText('')

        with open(name, 'w', encoding='UTF-8') as f:
            pass

        self.saveButton.setEnabled(True)
        self.fileNameInput.setPlaceholderText('Имя файла')
        self.IOfield.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec_())
