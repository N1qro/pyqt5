import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('main.ui', self) 

        self.isRunning = False
        self.remainingPebbles = 0

        self.takeButton.clicked.connect(self.makeAMove)
        self.setButton.clicked.connect(self.startGame)

    def updateLCD(self):
        self.remainingAmount.display(self.remainingPebbles)

    def startGame(self):
        if not self.isRunning:
            self.isRunning = True
            self.remainingPebbles = self.pebbleAmount.value()
            self.takeButton.setDisabled(False)
            self.winLabel.setText('')
            self.matchHistory.clear()
            self.updateLCD()

    def finishGame(self, playerWon=True):
        self.isRunning = False
        self.takeButton.setDisabled(True)
        self.remainingAmount.display(0)

        self.winLabel.setText(f'Победа {"игрока" if playerWon else "компьютера"}!')

    def makeAMove(self):
        remainingPebbles = self.remainingAmount.value()
        playerTakeAmount = self.takeAmount.value()

        remainingPebbles = max(remainingPebbles - playerTakeAmount, 0)
        self.matchHistory.appendPlainText(f'Игрок взял - {playerTakeAmount}')
        if not remainingPebbles:
            self.finishGame(playerWon=True)
        else:  # Bad AI that somehow works
            if remainingPebbles >= 10:
                aiTakeAmount = 3
            elif remainingPebbles in (4, 5, 8):
                aiTakeAmount = 1
            elif remainingPebbles in (6, 9):
                aiTakeAmount = 2
            elif remainingPebbles == 7:
                aiTakeAmount = 3
            else:
                aiTakeAmount = int(remainingPebbles)
                self.finishGame(playerWon=False)
        
        if remainingPebbles > 0:  # If AI needs to take any pebbles
            self.matchHistory.appendPlainText(f'Компьютер взял - {aiTakeAmount}')
            remainingPebbles -= aiTakeAmount
        self.remainingAmount.display(remainingPebbles)
            

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())