import sys

from itertools import zip_longest
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('main.ui', self)
        
        self.submitButton.clicked.connect(self.onClick)
    
    def onClick(self):
        leftWords = [elem.strip() for elem in self.leftTextField.toPlainText().split('\n') if elem]
        rightWords = [elem.strip() for elem in self.rightTextField.toPlainText().split('\n') if elem]

        possibilities = list()
        for line1, line2 in zip(leftWords, rightWords):
            forwardScan = list(map(lambda ltrs: ltrs[0] == ltrs[1], zip_longest(line1, line2)))
            backwardScan = list(map(lambda ltrs: ltrs[0] == ltrs[1], zip_longest(line1[::-1], line2[::-1])))

            poss1 = forwardScan.count(True) / len(forwardScan)
            poss2 = backwardScan.count(True) / len(backwardScan)

            possibilities.append(max(poss1, poss2))

        if possibilities:
            totalPlagiatpossibility = sum(possibilities) / len(possibilities)

            message = f'Код похож на {round(totalPlagiatpossibility * 100, 2)}%'
            if totalPlagiatpossibility  >= self.percentageInput.value() / 100:
                message += ' - Это плагиат.'
            self.statusbar.showMessage(message)

            redComponent = round(255 * totalPlagiatpossibility)
            greenComponent = round(255 * (1 - totalPlagiatpossibility))
            
            self.statusbar.setStyleSheet(f"""
                background-color: rgb({redComponent}, {greenComponent}, 0);
            """)

        else:
            self.statusbar.showMessage('Нам нечего сверять =)')
            self.statusbar.setStyleSheet("""
                background-color: rgb(101, 255, 5);
            """)
        
                


        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
