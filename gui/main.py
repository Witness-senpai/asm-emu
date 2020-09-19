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
    
    def __update_gui_conponents(self, reset=False):
        """
        Updating all components in GUI according to assembler state
        """
        self.__update_flags(reset=reset)
        self.__update_registers(reset=reset)
        self.__update_stack(reset=reset)
        self.__update_memory(reset=reset)

    def __update_flags(self, reset=False):
        """
        Updating flags in GUI according yo assembler state
        """
        flags = [self.assembler.flags[key] 
            for key in self.assembler.flags.keys()
        ]
        if reset:
            flags = [False for _ in self.assembler.flags]
        self.checkBox_Z.setChecked(flags[0])
        self.checkBox_C.setChecked(flags[1])
        self.checkBox_S.setChecked(flags[2])
        self.checkBox_P.setChecked(flags[3])
        self.checkBox_O.setChecked(flags[4])
    
    def __update_registers(self, reset=False):
        """
        Updating registers in GUI according yo assembler state
        """
        regs = [self.assembler.R[key]
            for key in self.assembler.R.keys()
        ]
        if reset:
            regs = [0 for _ in self.assembler.R]
        self.lcd_R1.display(regs[0])
        self.lcd_R2.display(regs[1])
        self.lcd_R3.display(regs[2])
        self.lcd_R4.display(regs[3])
        self.lcd_R5.display(regs[4])
        self.lcd_R6.display(regs[5])
        self.lcd_R7.display(regs[6])
        self.lcd_PC.display(regs[7])
        self.lcd_SP.display(regs[8])
    
    def __update_stack(self, reset=False):
        """
        Updating stack in GUI according yo assembler state
        """
        pass

    def __update_memory(self, reset=False):
        """
        Updating memory in GUI according yo assembler state
        """
        pass

    def btn_step_click(self):
        """
        Button for executing program step by step
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
        # If latest item for cmd part
        if self.assembler.R['PC'] == len(self.assembler.compiled_cmds) - 1:
            self.btn_step.setEnabled(False)
            self.btn_run.setEnabled(False)

        self.assembler.execute_code_by_step()
        self.__update_gui_conponents()
    
    def btn_run_click(self):
        """
        Button for executing all program
        """
        print("run")
        self.assembler.execute_all_code()
        
    def btn_reset_click(self):
        """
        Reset assembler and GUI to the start state
        """
        print("reset")
        self.assembler.reset_all()
        self.btn_step.setEnabled(True)
        self.btn_run.setEnabled(True)
        self.btn_load.setEnabled(True)
        self.__update_gui_conponents(reset=True)
    
    def btn_load_click(self):
        """
        Input programm from text field
        """
        text_program = self.textEdit_input.toPlainText()
        print(text_program)
        if text_program != '':
            load_result = self.assembler.input_text_program(
                text_program.upper()
            )
            if load_result == True:
                self.textEdit_input.setReadOnly(True)
                self.btn_load.setEnabled(False)
                self.load_program_to_mem()
            else:
                print(load_result)
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Load program error")
                msg.setInformativeText(load_result)
                msg.setWindowTitle("Error")
                msg.exec_()
    
    def load_program_to_mem(self):
        print(self.assembler.compiled_cmds)
        cmd_items = []
        for i, cmd in enumerate(self.assembler.memory):
            cmd_item = QtWidgets.QTreeWidgetItem()
            cmd_item.setText(0, hex(i).upper())
            cmd_item.setText(1, hex(int(cmd, 2)).upper())
            cmd_items.append(cmd_item)
        self.list_memory.addTopLevelItems(cmd_items)


if  __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()