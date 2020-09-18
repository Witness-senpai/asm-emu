from array import array

from .lexer import do_lex
from .asm_parser import Parser
from .compiler import Compiler
from .constants import (
    CMD_CODES,
    INPUT_BASE,
    CMDCODE_LENGTH,
    LITERAL_LENGTH,
    ADDRESS_LENGTH,
    REGISTER_LENGTH,
    FIRST_DATA_ADDRESS,
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
        [24-39] X3 -- address (Filling zeros if not using)
        [40-42] X4 -- number of register (Filling zeros if not using)
    
    Stack machine:
        Using stack for execution all opertions.
        3| 0 | 
        2| 0 |
        1| 0 |
        0| A | <<-- Stack Pointer
    """
    def __init__(self, compiled_cmds=None):
        # Bynary program from compiler
        self.compiled_cmds = compiled_cmds
        # List of stack, where will be executing all operations.
        self.__stack = [0, 0, 0, 0, 0]
        # List, witch using as memory space for commands and operands.
        self.__mem = array('i', [0 for _ in range(2**ADDRESS_LENGTH-1)])
        # Dictionary of common registers[from 1 to 2**REGISTER_LENGTH-1]
        # and also of system registers -- PC and SP
        self.__R = { 
            (i+1): 0 for i in range(2**REGISTER_LENGTH-1)
        }
        self.__R.update({ 
            'PC': 0, # Programm counter.
            'SP': 0, # Stack pointer
        })
        self.__flags = {# Dictionary of flags.
            'Z': False, # Zero
            'S': False, # Sign 
            'P': False, # Parity
            'C': False, # Carry
            'O': False, # Overflow
        }

    def reset_all(self):
        self.__init__(self.compiled_cmds)
    
    def input_text_program(self, program_text):
        """
        Input programm from simple text
        """
        tokens = do_lex(program_text)
        parser = Parser(tokens)
        if (parser.is_valid_code()):
            valid_cmd_lines = parser.valid_cmd_lines
            compiler = Compiler(valid_cmd_lines)
            compiler.compile()
            self.compiled_cmds = compiler.compiled_cmds

    def execute_code(self):
        """
        Main function for execution binary code
        """
        while self.__R['PC'] < len(self.compiled_cmds):
            print(self.__R)
            print(self.__stack)
            try:
                cmd = self.compiled_cmds[self.__R['PC']]
            except Exception as ex:
                print(ex)
            cmd_code = int(cmd[:CMDCODE_LENGTH], 2)
            literal  = int(cmd[CMDCODE_LENGTH:CMDCODE_LENGTH+LITERAL_LENGTH], 2)
            address  = int(cmd[CMDCODE_LENGTH+LITERAL_LENGTH:-REGISTER_LENGTH], 2)
            register = int(cmd[-REGISTER_LENGTH:], 2)

            if cmd_code == 1:
                self.__add()
            elif cmd_code == 2:
                self.__sub()
            elif cmd_code == 3:
                self.__inc()
            elif cmd_code == 4:
                self.__dec()
            elif cmd_code == 5:
                self.__push(
                    literal=literal,
                    address=address,
                    register=register,
                )
            elif cmd_code == 6:
                self.__pop(
                    address=address,
                    register=register,
                )
            elif cmd_code == 7:
                self.__cmp()
            elif cmd_code == 8:
                self.__not()
            elif cmd_code == 9:
                self.__or()
            elif cmd_code == 10:
                self.__and()
            elif cmd_code == 11:
                self.__xor()
            elif cmd_code == 12:
                self.__nor()
            elif cmd_code == 13:
                self.__shl()
            elif cmd_code == 14:
                self.__shr()
            elif cmd_code == 15:
                self.__jmp(new_pc=address)
            elif cmd_code == 16:
                self.__jc(new_pc=address)
            elif cmd_code == 17:
                self.__jz(new_pc=address)
            elif cmd_code == 18:
                self.__jp(new_pc=address)
            elif cmd_code == 19:
                self.__js(new_pc=address)
            elif cmd_code == 20:
                self.__jo(new_pc=address)
            elif cmd_code == 21:
                self.__njc(new_pc=address)
            elif cmd_code == 22:
                self.__njz(new_pc=address)
            elif cmd_code == 23:
                self.__njp(new_pc=address)
            elif cmd_code == 24:
                self.__njs(new_pc=address)
            elif cmd_code == 25:
                self.__njo(new_pc=address)
            elif cmd_code == 26:
                self.__nope()

    def __cmd_stack_push(self, el):
        self.__stack[self.__R['SP']] = el
        self.__R['SP'] += 1

    def __cmd_stack_pop(self):
        self.__stack[self.__R['SP']] = 0
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
        op1 = self.__cmd_stack_pop()
        op2 = self.__cmd_stack_pop()
        res = op2 - op1
        self.__update_flags(res)
        self.__push(
            literal=abs(res),
            address=0,
            register=0,
        )

    def __inc(self):
        """
        Increment of last stack element
        """
        op = self.__cmd_stack_pop()
        op += 1
        self.__cmd_stack_push(op)
        self.__update_flags(op)
        self.__R['PC'] += 1

    def __dec(self):
        """
        Decrement of last stack element
        """
        op = self.__cmd_stack_pop()
        op -= 1
        self.__cmd_stack_push(abs(op))
        self.__update_flags(op)
        self.__R['PC'] += 1
        
    def __push(self, literal, address, register):
        """
        Pushing element to stack as literal or from register or from memory
        """
        if (register != 0 and address == 2**ADDRESS_LENGTH - 1):
            address = self.__R[register] # Indirect addressing by register
            self.__cmd_stack_push(self.__mem[address])
        elif address == register == 0:
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
        if (register != 0 and address == 2**ADDRESS_LENGTH - 1) \
                or register == 0:
            if register != 0: # If indirect addressing by register
                address = self.__R[register]
            # If direct addressing by address
            self.__mem[address] = self.__cmd_stack_pop()
        elif address == 0:
            self.__R[register] = self.__cmd_stack_pop()
        elif register == 0:
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
        self.__R['PC'] += 1
    
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

    def __jmp(self, new_pc):
        """
        Go to the new PC obtained from the label
        """
        self.__R['PC'] = new_pc

    def __jc(self, new_pc):
        """
        Go to the new PC if carry flag
        """
        if self.__flags['C']:
            self.__R['PC'] = new_pc
        else:
            self.__R['PC'] += 1

    def __njc(self, new_pc):
        self.__flags['C'] = not self.__flags['C']
        self.__jc(new_pc)
        self.__flags['C'] = not self.__flags['C']

    def __jz(self, new_pc):
        """
        Go to the new PC if zero flag
        """
        if self.__flags['Z']:
            self.__R['PC'] = new_pc
        else:
            self.__R['PC'] += 1

    def __njz(self, new_pc):
        self.__flags['Z'] = not self.__flags['Z']
        self.__jz(new_pc)
        self.__flags['Z'] = not self.__flags['Z']

    def __jp(self, new_pc):
        """
        Go to the new PC if parity flag (even number)
        """
        if self.__flags['P']:
            self.__R['PC'] = new_pc
        else:
            self.__R['PC'] += 1

    def __njp(self, new_pc):
        self.__flags['P'] = not self.__flags['P']
        self.__jp(new_pc)
        self.__flags['P'] = not self.__flags['P']

    def __js(self, new_pc):
        """
        Go to the new PC if sign flag (number < 0)
        """
        if self.__flags['S']:
            self.__R['PC'] = new_pc
        else:
            self.__R['PC'] += 1
    
    def __njs(self, new_pc):
        self.__flags['S'] = not self.__flags['S']
        self.__js(new_pc)
        self.__flags['S'] = not self.__flags['S']

    def __jo(self, new_pc):
        """
        Go to the new PC if overflow flag
        """
        if self.__flags['O']:
            self.__R['PC'] = new_pc
        else:
            self.__R['PC'] += 1
    
    def __njo(self, new_pc):
        self.__flags['O'] = not self.__flags['O']
        self.__jo(new_pc)
        self.__flags['O'] = not self.__flags['O']

    def __nope(self):
        """
        Skip clock and just increment PC
        """
        self.__R['PC'] += 1