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

        # Used colors
        self.qt_white_color = QtGui.QColor(255, 255, 255)
        self.qt_green_color = QtGui.QColor(127, 201, 127)

        # Using the previous item to correctly visualize
        # step by step execution program
        self.previous_mem_item = None

        self.list_memory.setHeaderLabels(['addr', 'data', 'cmd'])
        self.list_stack.setHeaderLabels(['SP', 'data'])

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
        self.checkBox_S.setChecked(flags[1])
        self.checkBox_P.setChecked(flags[2])
        self.checkBox_C.setChecked(flags[3])
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
        print(self.assembler.stack)
        self.list_stack.clear()
        stack_items = []
        for i, cmd in enumerate(self.assembler.stack):
            cmd_item = QtWidgets.QTreeWidgetItem()
            cmd_item.setText(0, hex(i).upper())
            cmd_item.setText(1, hex(cmd).upper())
            stack_items.append(cmd_item)
        self.list_stack.addTopLevelItems(stack_items[::-1])

        # Colorize current item
        current_stack_item = self.list_stack.topLevelItem(
            len(self.assembler.stack) - self.assembler.R['SP'] - 1
        )
        current_stack_item.setBackground(0, (self.qt_green_color))
        current_stack_item.setBackground(1, (self.qt_green_color))


    def __update_memory(self, reset=False):
        """
        Updating memory in GUI according yo assembler state
        """
        print(self.assembler.memory)
        self.list_memory.clear()
        memory_items = []
        for i, cmd in enumerate(self.assembler.memory):
            cmd_item = QtWidgets.QTreeWidgetItem()
            cmd_item.setText(0, hex(i).upper())
            cmd_item.setText(1, hex(int(cmd, 2)).upper())
            cmd_item.setText(2, 
                            (self.assembler.valid_cmd_lines[i] \
                                if i < len(self.assembler.valid_cmd_lines) else '-')
                            .upper())
            memory_items.append(cmd_item)
        self.list_memory.addTopLevelItems(memory_items)

        # Colorize current item
        current_memory_item = self.list_memory.topLevelItem(
            self.assembler.R['PC']
        )
        current_memory_item.setBackground(0, (self.qt_green_color))
        current_memory_item.setBackground(1, (self.qt_green_color))
        current_memory_item.setBackground(2, (self.qt_green_color))

    def btn_step_click(self):
        """
        Button for executing program step by step
        """
        print("step")
        if self.assembler.R['PC'] >= len(self.assembler.compiled_cmds):
            self.btn_step.setEnabled(False)
            self.btn_run.setEnabled(False)
        else:
            self.assembler.execute_code_by_step()
            self.__update_gui_conponents()
    
    def btn_run_click(self):
        """
        Button for executing all program
        """
        print("run")
        self.assembler.execute_all_code()
        self.btn_step.setEnabled(False)
        self.btn_run.setEnabled(False)
        self.__update_gui_conponents()

    def btn_reset_click(self):
        """
        Reset assembler and GUI to the start state
        """
        print("reset")
        self.assembler.reset_all()
        self.btn_step.setEnabled(True)
        self.btn_run.setEnabled(True)
        self.btn_load.setEnabled(True)
        self.textEdit_input.setReadOnly(False)
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
                self.__update_memory()
                self.__update_stack()
            else:
                print(load_result)
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Program load error")
                msg.setInformativeText(load_result)
                msg.setWindowTitle("Error")
                msg.exec_()


if  __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()