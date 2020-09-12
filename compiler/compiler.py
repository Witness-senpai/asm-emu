

class Compiler():
    def __init__(valid_cmd_lines):
        self.LITERAL_LENGTH = 8
        self.ADDRESS_LENGTH = 8
        self.CMD_LENGTH = 4
        self.__cmd_codes = {
            'ADD' : '0001',
            'SUB' : '0002',
            'PUSH': '1000',
            'POP' : '1001',
            'CMD' : '1002',
            'NOT' : '1003',
            'OR'  : '1004',
            'AND' : '1005',
            'XOR' : '1006',
            'NOR' : '1007',
            'SHL' : '2000',
            'SHR' : '2001',
            'JMP' : '3000',
            'JC'  : '3001',
            'JZ'  : '3002',
        }
        self.valid_cmd_lines = valid_cmd_lines
        self.compiled_cmds = [] # Result of compilation

    def get_cmd_code(self, cmd):
        # 0-3   -> command code
        # 4-11  -> literal
        # 12-19 -> address
        compiled_cmd_lines = []
        for cmd_line in self.valid_cmd_lines:
            cmd_code = self.get_cmd_code(cmd_line[0]) \
                .zfill(self.CMD_LENGTH) 
                
            if cmd_line[1][1] == 'LITERAL':
                literal_code = str(int(cmd_line[0][1:], 16)) \
                    .zfill(self.LITERAL_LENGTH) 
            elif cmd_line[1][1] == 'ADDR':
                address_code = int(cmd_line[0][1:], 16) \
                    .zfill(self.ADDRESS_LENGTH) 
            compiled_cmd_lines = cmd_code \
                + literal_code + address_code
        
        return compiled_cmd_lines

    def __compile_line(self, cmd_line):

        
    
    def compile(self):
