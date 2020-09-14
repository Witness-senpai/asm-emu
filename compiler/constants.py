INPUT_BASE = 16
CMDCODE_LENGTH = 8
LITERAL_LENGTH = 16
ADDRESS_LENGTH = 8

CMD_CODES = {
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