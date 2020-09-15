INPUT_BASE = 16
CMDCODE_LENGTH = 8
LITERAL_LENGTH = 16
ADDRESS_LENGTH = 8
REGISTER_LENGTH = 3
MEMORY_RATIO = 4
FIRST_DATA_ADDRESS = (2**ADDRESS_LENGTH) / MEMORY_RATIO

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
    'NOR' : '10',
    'SHL' : '11',
    'SHR' : '12',
    'JMP' : '13',
    'JC'  : '14',
    'JZ'  : '15',
    'ZP'  : '16',
    'JS'  : '17',
    'JO'  : '18',
}