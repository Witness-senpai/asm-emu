import numpy as np

from constants import (
    CMD_CODES,
    INPUT_BASE,
    CMDCODE_LENGTH,
    LITERAL_LENGTH,
    ADDRESS_LENGTH,
)


class Assembler():
    """
    The assembler language class, that's emulating execution of machine code.
    Features:
        * Fon Neiman architecture;
        * RISC comands format;
        * Using stack machine for execution of code

    Fon Neiman architecture:
        Using variable self.__mem as common memory space
        for comands and data.



    Inputting RISC comands format:
        X1_X2_X3, 32 bits length
        [0-7]   X1 -- code of command (see constants.py)
        [8-23]  X2 -- literal (Filling zeros if not exists)
        [24-31] X3 -- address (Filling zeros if not exists)
    
    Stack machine:
        
    """
    def __init__(self, compiled_cmds, jumps):
        self.__REGS_N = 8
        self.__R = { # Dictionary of system registers.
            str(i): 0 for i in range(self.__REGS_N)
        }
        self.__regs = { 
            'A': False,
            'B': False,
            'C': False,
            'D': False,
            'PC': 0, # Programm counter.
            'SP': 0, # Stack pointer.
        } 
        self.__flags = { # Dictionary of flags.
            'Z': False,
            'S': False,
            'P': False,
            'C': False,
            'AC': False,
        } 
        # List of stack, where will be executing all operations.
        self.__stack = [0, 0, 0, 0, 0] 
        # List, witch using as memory space for commands and operands.
        self.__mem = np.zeros(2**ADDRESS_LENGTH - 1, dtype=int)
        self.compiled_cmds = compiled_cmds
        self.jumps = jumps
    
    def input_program(self, compiled_cmds, jumps):
        self.compiled_cmds = compiled_cmds
        self.jumps = jumps
    
    def execute_code(self):
        for cmd in self.compiled_cmds: 
            # TODO: hardcode
            cmd_code = int(cmd, 0) & 0b11111111000000000000000000000000
            literal = int(cmd, 0) & 0b00000000111111111111111100000000
            address = int(cmd, 0) & 0b00000000000000000000000011111111
            
            if cmd_code == 1:
                self.__add()
            elif cmd_code == 2:
                self.__sub()
            elif cmd_code == 3:
                self.__push(address=address)
            elif cmd_code == 4:
                self.__pop()
            elif cmd_code == 5:
                self.__cmp()
            """
            elif cmd_code == 6:
                self.__not()
            elif cmd_code == 7:
                self.__or()
            elif cmd_code == 8:
                self.__and()
            elif cmd_code == 9:
                self.__xor()
            elif cmd_code == 10:
                self.__nor()
            elif cmd_code == 11:
                self.__shl()
            elif cmd_code == 12:
                self.__shr()
            elif cmd_code == 13:
                self.__jmp()
            elif cmd_code == 14:
                self.__jc()
            elif cmd_code == 15:
                self.__jz()"""

    def __cmd_stack_push(self, el):
        self.__stack[self.__regs['SP']] = el
        self.__regs['SP'] + 1

    def __cmd_stack_pop(self):
        self.__regs['SP'] - 1
        return self.__stack[self.__regs['SP']]

    def __update_flags(self):
        stack_head = self.__stack[-1]
        if stack_head == 0:
            pass    

    def __add(self):
        op1 = self.__stack.pop()
        op2 = self.__stack.pop()
        res = int(op1, 0) + int(op2, 0)
        self.__push(literal=res)
    
    def __sub(self):
        op1 = self.__stack.pop()
        op2 = self.__stack.pop()
        res = int(op1, 0) - int(op2, 0)
        self.__push(literal=res)

    def __push(self, address=None, literal=None, register=None):
        if address != None:
            self.__cmd_stack_push(self.__mem[address])
        elif literal != None:
            self.__cmd_stack_push(literal)
        elif register != None:
            pass
             # TODO: Regs support
        else:
            print('Empty stack!')
        
    def __pop(self, address=None, register=None):
        if len(self.__stack) == 0:
            print('Empty stack!')
        elif address != None:
            self.__mem[address] = self.__cmd_stack_pop()
        elif register != None:
            pass
            # TODO: Regs support
    
    def __cmp(self):
        pass


