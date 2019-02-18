from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class InputState:
    LOWER = 0
    CAPITAL = 1


class KeyButton(QPushButton):
    sigKeyButtonClicked = pyqtSignal()

    def __init__(self, key, resize = False):
        super(KeyButton, self).__init__()

        self._key = key
        if resize == True:
            self._activeSize = QSize(80,80)
        else:
            self._activeSize = self.sizeHint()
        self.clicked.connect(self.emitKey)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))


    def emitKey(self):
        self.sigKeyButtonClicked.emit()

    def enterEvent(self, event):
        self.setFixedSize(self._activeSize)

    def leaveEvent(self, event):
        self.setFixedSize(self.sizeHint())

    def sizeHint(self):
        return QSize(70, 70)

class VirtualKeyboard(QWidget):
    
    #sigKeyButtonClicked = pyqtSignal() code original contient cette ligne, n'est jamais utilisee. celle utilisee appartient a une autre classe
    sigInputString = pyqtSignal(str)

    def __init__(self, resize = False):
        super(VirtualKeyboard, self).__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.setFocusPolicy(Qt.ClickFocus)

        self.setGeometry(200,550,900,500)

        self.globalLayout = QVBoxLayout(self)
        self.keysLayout = QGridLayout()
        self.buttonLayout = QHBoxLayout()

        self.keyListByLines = [
                    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                    ['a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                    ['q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm'],
                    ['w', 'x', 'c', 'v', 'b', 'n', '_', '.', '/', ' '],
                ]
        self.inputString = ""
        self.state = InputState.LOWER

        self.stateButton = QPushButton()
        self.stateButton.setText('Maj.')
        self.backButton = QPushButton()
        self.backButton.setText('<-')
        self.okButton = QPushButton()
        self.okButton.setText('OK')
        self.atButton = QPushButton()
        self.atButton.setText("@")

        for lineIndex, line in enumerate(self.keyListByLines):
            for keyIndex, key in enumerate(line):
                buttonName = "keyButton" + key.capitalize()
                self.__setattr__(buttonName, KeyButton(key,resize))
                self.keysLayout.addWidget(self.getButtonByKey(key), self.keyListByLines.index(line), line.index(key))
                self.getButtonByKey(key).setText(key)
                self.getButtonByKey(key).sigKeyButtonClicked.connect(lambda v=key : self.addInputByKey(v))
                self.keysLayout.setColumnMinimumWidth(keyIndex, 50)
            self.keysLayout.setRowMinimumHeight(lineIndex, 50)

        self.stateButton.clicked.connect(self.switchState)
        self.backButton.clicked.connect(self.backspace)
        self.okButton.clicked.connect(self.ok) 
        self.atButton.clicked.connect(self.emitat)


        self.buttonLayout.addWidget(self.atButton)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.stateButton)
        self.buttonLayout.addWidget(self.okButton)

        self.globalLayout.addLayout(self.keysLayout)

        self.globalLayout.addLayout(self.buttonLayout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))


    def enterEvent(self, event):
        print ("Mouse Entered")
        super(VirtualKeyboard, self).enterEvent(event)

    def leaveEvent(self, event):
        print("Mouse Left")
        self.hide()
        
        super(VirtualKeyboard, self).enterEvent(event)
        
    def getButtonByKey(self, key):
        return getattr(self, "keyButton" + key.capitalize())

    def getLineForButtonByKey(self, key):
        return [key in keyList for keyList in self.keyListByLines].index(True)

    def switchState(self):
        self.state = not self.state  
        
        if self.state:
            self.stateButton.setText('Min.')
            for i in range(len(self.keyListByLines)):
                for j in range(len(self.keyListByLines[i])):
                    self.getButtonByKey(self.keyListByLines[i][j]).setText(self.keyListByLines[i][j].upper())

        else:
            self.stateButton.setText('Maj.')   
            for i in range(len(self.keyListByLines)):
                for j in range(len(self.keyListByLines[i])):
                    self.getButtonByKey(self.keyListByLines[i][j]).setText(self.keyListByLines[i][j].lower())

    

    def addInputByKey(self, key):
        self.inputString += (key.lower(), key.capitalize())[self.state]
        self.emitInputString()

    def backspace(self):
        self.inputString = self.inputString[:-1]
        self.emitInputString()

    def emitInputString(self):
        self.sigInputString.emit(self.inputString)

    def emitat(self): #ne convient pas vraiment a notre utilisation puisque on le relie directement a un champ de texte
        self.addInputByKey('@')

    def sizeHint(self):
        return QSize(480,272)

    def ok(self):
        self.hide()    


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    win = VirtualKeyboard()
    win.show()
    app.exec_()
