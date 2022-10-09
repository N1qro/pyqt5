import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic


class FileManager(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('main.ui', self)

        self.numbers = list()
        self.submitButton.clicked.connect(self.onClick)

    def onClick(self) -> None:
        try:
            self.filename = self.fileName.text()
            with open(self.filename, 'r') as f:
                for line in f.readlines():
                    for word in line.split():
                        if not word.isdigit():
                            raise ValueError
                        self.numbers.append(int(word))
        except FileNotFoundError:
            self.outputText.setText(f'Файл "{self.filename}" не найден.')
        except ValueError:
            self.outputText.setText(f'В файле "{self.filename}" содержутся некорректные данные')
        else:
            self.maxValue.setValue(max(self.numbers))
            self.minValue.setValue(min(self.numbers))
            
            average = sum(self.numbers) / len(self.numbers)
            self.averageValue.setValue(average)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileManager()
    window.show()
    sys.exit(app.exec_())
