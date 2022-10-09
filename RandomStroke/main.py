import sys
import os
import random

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('main.ui', self)

        if not os.path.exists('file.txt'):
            print('"file.txt" не был найден в директории. Приложение не будет запущенно.')
            sys.exit(0)
        elif not os.path.getsize('file.txt'):
            print('Файл пустой. Приложение запущенно не будет')
            sys.exit(0)

        with open('file.txt', encoding='UTF-8') as f:
            self.strokes = list(map(str.strip, f.readlines()))

        if len(self.strokes) <= 1:
            print('В файле всего 1 строка. Приложение заблокирует кнопку после её вывода.')
            self.btn_get.clicked.connect(self.onDClick)
        else:
            self.btn_get.clicked.connect(self.onClick)
    
    def onDClick(self) -> None:
        self.output.setText(self.strokes[0])
        self.btn_get.setEnabled(False)

    def onClick(self) -> None:
        wasPreviously = self.output.text()
        randomStroke = random.choice(self.strokes)

        while wasPreviously == randomStroke:
            randomStroke = random.choice(self.strokes)
        
        self.output.setText(randomStroke)

    

        
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
