import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gui/disign.ui", self)

        # Set app icon 
        app_icon = QtGui.QIcon()
        app_icon.addFile('gui/icons/32x32.png', QtCore.QSize(32,32))
        app_icon.addFile('gui/icons/64x64.png', QtCore.QSize(64,64))
        app_icon.addFile('gui/icons/128x128.png', QtCore.QSize(128,128))
        app_icon.addFile('gui/icons/256x256.png', QtCore.QSize(256,256))
        app.setWindowIcon(app_icon)

        # Init buttons
        self.btn_step.clicked.connect(self.btn_step_click)
        self.btn_run.clicked.connect(self.btn_run_click)
        self.btn_reset.clicked.connect(self.btn_reset_click)
        #self.textEdit_input.clicked.connect(self.textEdit_input_click)
   
    def btn_step_click(self):
        print("step")
    
    def btn_run_click(self):
        print("run")
        
    def btn_reset_click(self):
        print("reset")

if  __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()