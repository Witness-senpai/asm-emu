from constants import (
    CMD_CODES,
    INPUT_BASE,
    CMDCODE_LENGTH,
    LITERAL_LENGTH,
    ADDRESS_LENGTH,
    REGISTER_LENGTH,
)

class Compiler:
    """
    A Compiler class, that's translates valid command
    to machine code and setts jump addresses.
    """
    def __init__(self, valid_cmd_lines):
        self.valid_cmd_lines = valid_cmd_lines
        self.jumps = {} # Dict of jumsp: label->address
        self.compiled_cmds = [] # Result of compilation

    def compile(self):
        """
        Detect all jumps and their addresses
        """
        for n_line, cmd_line in enumerate(self.valid_cmd_lines):
            if cmd_line[0][1] == 'LABEL':
                self.jumps.update({
                    cmd_line[0][0]: n_line
            })
        for n_line, cmd_line in enumerate(self.valid_cmd_lines):
            literal_code = ''.zfill(LITERAL_LENGTH)
            address_code = ''.zfill(ADDRESS_LENGTH)
            register_code = ''.zfill(REGISTER_LENGTH)
            if cmd_line[0][1] == 'LABEL':
                continue
            else:
                cmd_code = self.__to_bin(
                    CMD_CODES[cmd_line[0][1]],
                    base=10
                ).zfill(CMDCODE_LENGTH)
                if len(cmd_line) == 1: # For comands w/o addresses and literals
                    pass
                elif 'J' in cmd_line[0][1]: # For all jumps
                    try:
                        jump_address = self.jumps[cmd_line[1][0]] \
                            if cmd_line[1][1] == 'LABEL' else cmd_line[1][0]
                    except Exception as ex:
                        print(ex)
                    address_code = self.__to_bin(
                            str(jump_address),
                            base=10,
                        ).zfill(ADDRESS_LENGTH)
                elif cmd_line[1][1] == 'LITERAL':
                    literal_code = self.__to_bin(cmd_line[1][0]) \
                        .zfill(LITERAL_LENGTH)
                elif cmd_line[1][1] == 'ADDR':
                    # If indetect addressing by register
                    if 'R' in cmd_line[1][0]:
                        register_code = self.__to_bin(cmd_line[1][0][1]) \
                            .zfill(REGISTER_LENGTH)
                        # Address = 1..1 as a signal for assembler, that's a
                        # indetect addressing by register
                        address_code = ''.ljust(ADDRESS_LENGTH, '1')
                    else:
                        address_code = self.__to_bin(cmd_line[1][0]) \
                            .zfill(ADDRESS_LENGTH)
                elif cmd_line[1][1] == 'REG':
                    register_code = self.__to_bin(cmd_line[1][0][1]) \
                        .zfill(REGISTER_LENGTH)

                self.compiled_cmds.append(
                    cmd_code 
                    + literal_code  
                    + address_code
                    + register_code
                )
    
    def __to_bin(self, num, base=None):
        """
        Converting address or literal to binary number in str format
        """
        if base is None:
            base = INPUT_BASE
        # [2:] -- for removing '0b' from binary
        return str(bin(int(num, base)))[2:]
