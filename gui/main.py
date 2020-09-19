import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

from pyasm.assembler_lang import Assembler


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
        self.btn_load.clicked.connect(self.btn_load_click)

        self.list_memory.setHeaderLabels(['addr','data'])

        # Init Assembler class
        self.assembler = Assembler()

    def btn_step_click(self):
        """
        Button for xecuting program step by step
        """
        print("step")
        # Back to white for previous item
        if self.assembler.R['PC'] != 0:
            item = self.list_memory.topLevelItem(self.assembler.R['PC']-1)
            item.setBackground(0, (QtGui.QColor(255, 255, 255)))
            item.setBackground(1, (QtGui.QColor(255, 255, 255)))
        # Colorize current item
        item = self.list_memory.topLevelItem(self.assembler.R['PC'])
        item.setBackground(0, (QtGui.QColor(127, 201, 127)))
        item.setBackground(1, (QtGui.QColor(127, 201, 127)))
        print(item)
        self.assembler.R['PC'] += 1
    
    def btn_run_click(self):
        """
        Button for executing all program
        """
        print("run")
        self.assembler.execute_code()
        
    def btn_reset_click(self):
        """
        Reset all flags, registers, memory
        """
        print("reset")
        self.assembler.reset_all()
    
    def btn_load_click(self):
        """
        Input programm from text field
        """
        text_program = self.textEdit_input.toPlainText()
        print(text_program)
        if text_program != '':
            self.assembler.input_text_program(text_program.upper())
        self.textEdit_input.setReadOnly(True)
        self.btn_load.setEnabled(False)

        self.load_program_to_mem()
    
    def load_program_to_mem(self):
        print(self.assembler.compiled_cmds)
        cmd_items = []
        for i, cmd in enumerate(self.assembler.memory):
            cmd_item = QtWidgets.QTreeWidgetItem()
            cmd_item.setText(0, hex(i).upper())
            cmd_item.setText(1, hex(int(cmd, 2)).upper())
            cmd_items.append(cmd_item)
        self.list_memory.addTopLevelItems(cmd_items)
    
    def update_memory(self):
        pass

if  __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()