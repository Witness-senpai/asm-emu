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
    'INC' : '3',
    'DEC' : '4',
    'PUSH': '5',
    'POP' : '6',
    'CMP' : '7',
    'NOT' : '8',
    'OR'  : '9',
    'AND' : '10',
    'XOR' : '11',
    'NOR' : '12',
    'SHL' : '13',
    'SHR' : '14',
    'JMP' : '15',
    'JC'  : '16',
    'JZ'  : '17',
    'ZP'  : '18',
    'JS'  : '19',
    'JO'  : '20',
    'NJC'  : '21',
    'NJZ'  : '22',
    'NZP'  : '23',
    'NJS'  : '24',
    'NJO'  : '25',
    'NOPE' : '26',
    'MUL'  : '27',
}