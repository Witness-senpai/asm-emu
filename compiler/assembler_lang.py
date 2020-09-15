import numpy as np

from constants import (
    CMD_CODES,
    INPUT_BASE,
    CMDCODE_LENGTH,
    LITERAL_LENGTH,
    ADDRESS_LENGTH,
    REGISTER_LENGTH,
)


class Assembler():
    """
    The assembler language class, that's emulating execution of machine code.
    Features:
        * Fon Neiman architecture;
        * RISC comands format;
        * Using stack machine for execution of code

    Fon Neiman architecture:
        All memory space there are in self.__mem, but logical
        separating on two parts: for commands and data.
        Memory ratio for commands and data by default -- 1:3
        Addresses for commands: [0, FIRST_DATA_ADDRESS - 1]
        Addresses for data: [FIRST_DATA_ADDRESS: 2**ADDRESS_LENGTH-1]

    Inputting RISC commands format:
        X1_X2_X3_X4, 35 bits length
        [0-7]   X1 -- code of command (see constants.py)
        [8-23]  X2 -- literal (Filling zeros if not using)
        [24-31] X3 -- address (Filling zeros if not using)
        [32-34] X4 -- number of register (Filling zeros if not using)
    
    Stack machine:
        Using stack for execution all opertions.
        3|   | 
        2|   |
        1| - |
        0|_A_| <<-- Stack Pointer
    """
    def __init__(self, compiled_cmds, jumps):
        # Bynary program and jumps addresses from compiler
        self.compiled_cmds = compiled_cmds
        self.jumps = jumps
        # List of stack, where will be executing all operations.
        self.__stack = [0, 0, 0, 0, 0]
        # List, witch using as memory space for commands and operands.
        self.__mem = np.zeros(2**ADDRESS_LENGTH, dtype=int)
        # Dictionary of common registers[from 1 to 2**REGISTER_LENGTH-1]
        # and also of system registers -- PC and SP
        self.__R = { 
            (i+1): 0 for i in range(2**REGISTER_LENGTH-1)
        }
        self.__R.update(
            { 
                'PC': 0, # Programm counter.
                'SP': 0, # Stack pointer
            }
        )
        self.__flags = {# Dictionary of flags.
            'Z': False, # Zero
            'S': False, # Sign 
            'P': False, # Parity
            'C': False, # Carry
            'O': False, # Overflow
        }

    
    def input_program(self, compiled_cmds, jumps):
        self.compiled_cmds = compiled_cmds
        self.jumps = jumps
    
    def execute_code(self):
        while self.__R['PC'] <= len(self.compiled_cmds):
            cmd = self.compiled_cmds[self.__R['PC']]

            cmd_code = int(cmd[:CMDCODE_LENGTH], 2)
            literal  = int(cmd[CMDCODE_LENGTH:CMDCODE_LENGTH+LITERAL_LENGTH], 2)
            address  = int(cmd[CMDCODE_LENGTH+LITERAL_LENGTH:-REGISTER_LENGTH], 2)
            register = int(cmd[-REGISTER_LENGTH:], 2)

            if cmd_code == 1:
                self.__add()
            elif cmd_code == 2:
                self.__sub()
            elif cmd_code == 3:
                self.__push(
                    literal=literal,
                    address=address,
                    register=register,
                )
            elif cmd_code == 4:
                self.__pop(
                    address=address,
                    register=register,
                )
            elif cmd_code == 5:
                self.__cmp()
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
                self.__jmp(address=address)
            elif cmd_code == 14:
                self.__jc(address=address)
            elif cmd_code == 15:
                self.__jz(address=address)
            elif cmd_code == 16:
                self.__jp(address=address)
            elif cmd_code == 17:
                self.__js(address=address)
            elif cmd_code == 18:
                self.__jo(address=address)

    def __cmd_stack_push(self, el):
        self.__stack[self.__R['SP']] = el
        self.__R['SP'] += 1

    def __cmd_stack_pop(self):
        self.__R['SP'] -= 1
        return self.__stack[self.__R['SP']]

    def __update_flags(self, res):
        """
        Updating flags depends of res
        """
        if res == 0:
            self.__flags['Z'] = True
        else:
            self.__flags['Z'] = False

        if res < 0:
            self.__flags['S'] = True
        else:
            self.__flags['S'] = False
        
        if res % 2 == 0:
            self.__flags['P'] = True
        else:
            self.__flags['P'] = False


    def __add(self):
        """
        Addition of the last elements of the stack.
        Result also pushing to the stack.
        """        
        op1 = self.__cmd_stack_pop()
        op2 = self.__cmd_stack_pop()
        res = int(str(op1), 0) + int(str(op2), 0)
        self.__update_flags(res)
        self.__push(
                    literal=res,
                    address=0,
                    register=0,
                )
    
    def __sub(self):
        """
        Subtraction of the last elements of the stack.
        Result also pushing to the stack.
        """
        res = self.__cmp()
        self.__push(
            literal=res,
            address=0,
            register=0,
        )

    def __push(self, literal, address, register):
        """
        Pushing element to stack as literal or from register or from memory
        """
        if address == register == 0:
            self.__cmd_stack_push(literal)
        elif literal == register == 0:
            self.__cmd_stack_push(self.__mem[address])
        elif address == literal == 0:
            self.__cmd_stack_push(self.__R[register])
        else:
            print('Empty stack!')
        self.__R['PC'] += 1
        
    def __pop(self, address, register):
        """
        Moving last element of stack to register or to memory
        """
        if register == 0:
            self.__mem[address] = self.__cmd_stack_pop()
        elif address == 0:
            self.__R[register] = self.__cmd_stack_pop()
        self.__R['PC'] += 1
    
    def __cmp(self):
        """
        Comparing last two numbers on stack
        """
        op1 = self.__cmd_stack_pop()
        op2 = self.__cmd_stack_pop()
        res = op2 - op1
        self.__update_flags(res)
        return abs(res)
    
    def __not(self):
        """
        Logical NOT
        """
        op = self.__cmd_stack_pop()
        res = ~op
        self.__update_flags(res)
        self.__push(
            literal=res,
            address=0,
            register=0,
        )
    
    def __or(self):
        """
        Logical OR
        """
        op1 = self.__cmd_stack_pop()
        op2 = self.__cmd_stack_pop()
        res = op1 | op2
        self.__update_flags(res)
        self.__push(
            literal=res,
            address=0,
            register=0,
        )

    def __and(self):
        """
        Logical AND
        """
        op1 = self.__cmd_stack_pop()
        op2 = self.__cmd_stack_pop()
        res = op1 & op2
        self.__update_flags(res)
        self.__push(
            literal=res,
            address=0,
            register=0,
        )

    def __xor(self):
        """
        Logical XOR
        """
        op1 = self.__cmd_stack_pop()
        op2 = self.__cmd_stack_pop()
        res = op1 ^ op2
        self.__update_flags(res)
        self.__push(
            literal=res,
            address=0,
            register=0,
        )

    def __nor(self):
        """
        Logical NOR
        """
        op1 = self.__cmd_stack_pop()
        op2 = self.__cmd_stack_pop()
        res = ~(op1 | op2)
        self.__update_flags(res)
        self.__push(
            literal=res,
            address=0,
            register=0,
        )

    def __shl(self):
        """
        Logical left shift by 1
        """
        op = self.__cmd_stack_pop()
        res = op << 1
        self.__update_flags(res)
        self.__push(
            literal=res,
            address=0,
            register=0,
        )

    def __shr(self):
        """
        Logical right shift by 1
        """
        op = self.__cmd_stack_pop()
        res = op >> 1
        self.__update_flags(res)
        self.__push(
            literal=res,
            address=0,
            register=0,
        )

    def __jmp(self, address):
        """
        Go to the address obtained from the label
        """
        # In this case, address -- line of asm program
        self.__R['PC'] = address

    def __jc(self, address):
        """
        Go to the address if carry flag
        """
        # In this case, address -- line of asm program
        if self.__flags['C']:
            self.__R['PC'] = address
        else:
            self.__R['PC'] += 1

    def __jz(self, address):
        """
        Go to the address if zero flag
        """
        # In this case, address -- line of asm program
        if self.__flags['Z']:
            self.__R['PC'] = address
        else:
            self.__R['PC'] += 1

    def __jp(self, address):
        """
        Go to the address if parity flag (even number)
        """
        # In this case, address -- line of asm program
        if self.__flags['C']:
            self.__R['PC'] = address
        else:
            self.__R['PC'] += 1

    def __js(self, address):
        """
        Go to the address if sign flag (number < 0)
        """
        # In this case, address -- line of asm program
        if self.__flags['Z']:
            self.__R['PC'] = address
        else:
            self.__R['PC'] += 1

    def __jo(self, address):
        """
        Go to the address if overflow flag
        """
        # In this case, address -- line of asm program
        if self.__flags['Z']:
            self.__R['PC'] = address
        else:
            self.__R['PC'] += 1