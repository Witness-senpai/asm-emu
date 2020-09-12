

class Compiler:
    """
    A Compiler class, that's translates valid commands to machine code.
    Also, compiler setts jump addresses
    """
    def __init__(self, valid_cmd_lines):
        self.INPUT_BASE = 16
        self.CMDCODE_LENGTH = 8
        self.LITERAL_LENGTH = 16
        self.ADDRESS_LENGTH = 8
        self.CMD_LENGTH = 4
        self.jumps = {} # Dict of jumsp: label->address
        self.valid_cmd_lines = valid_cmd_lines
        self.compiled_cmds = [] # Result of compilation
        self.__cmd_codes = {
            'ADD' : '1',
            'SUB' : '2',
            'PUSH': '3',
            'POP' : '4',
            'CMP' : '5',
            'NOT' : '6',
            'OR'  : '7',
            'AND' : '8',
            'XOR' : '9',
            'NOR' : 'A',
            'SHL' : 'B',
            'SHR' : 'C',
            'JMP' : 'D',
            'JC'  : 'E',
            'JZ'  : 'F',
        }

    def compile(self):
        for cmd_line in self.valid_cmd_lines:
            literal_code = ''.zfill(self.LITERAL_LENGTH)
            address_code = ''.zfill(self.ADDRESS_LENGTH)
            if cmd_line[0][1] == 'LABEL':
                self.jumps.update({
                    cmd_line[0][0]: len(self.compiled_cmds)
                })
            else:
                cmd_code = self.__to_bin(
                    self.__cmd_codes[cmd_line[0][1]]
                )
                if len(cmd_line) == 1: # For comands w/o addresses and literals
                    pass
                elif cmd_line[1][1] == 'LABEL':
                    address_code = str(bin(self.jumps[cmd_line[1][0]]))[2:] \
                        .zfill(self.LITERAL_LENGTH)
                elif cmd_line[1][1] == 'LITERAL':
                    # [2:] - for removing '0b' in binary number
                    literal_code = self.__to_bin(cmd_line[1][0]) \
                        .zfill(self.LITERAL_LENGTH)
                elif cmd_line[1][1] == 'ADDR':
                    address_code = self.__to_bin(cmd_line[1][0]) \
                        .zfill(self.ADDRESS_LENGTH)
                elif cmd_line[1][1] == 'REG':
                    pass
                self.compiled_cmds.append(
                    cmd_code + literal_code + address_code
                )
    
    def __to_bin(self, num, base=None):
        """
        Converting address or literal to binary number in str format
        """
        if base is None:
            base = self.INPUT_BASE
        # [2:] -- for removing 0b from binary
        return str(bin(int(num, base)))[2:]
