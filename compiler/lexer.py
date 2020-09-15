import re
import sys


token_exprs = [
    (r'[\n]+',                  'NLINE'), # New lines
    (r'[ \t]+',                    None), # Spaces, tabs between comands
    (r';[^\n]*',                   None), # Comment 

    (r'PUSH',                    "PUSH"),
    (r'POP',                      "POP"),

    (r'R[1-7]',                  "REG"), # One of registers R1-R7

    (r'CMP',                      "CMP"),

    (r'JMP',                      "JMP"),
    (r'JZ',                        "JZ"),
    (r'JC',                        "JC"),
    (r'JS',                        "JS"),
    (r'JP',                        "JP"),
    (r'JO',                        "JO"),

    (r'ADD',                      "ADD"),
    (r'SUB',                      "SUB"),
    (r'INC',                      "INC"),
    (r'DEC',                      "DEC"),
 
    (r'SHL',                      "SHL"), # Shift left
    (r'SHR',                      "SHR"), # Shift right
 
    (r'AND',                      "AND"),
    (r'OR',                        "OR"),
    (r'NOR',                      "NOR"),
    (r'XOR',                      "XOR"),     
    (r'NOT',                      "NOT"),

    (r'#[0-9A-F]+',           "LITERAL"),
    (r'@[0-9A-FR\[1-7\]]+',      "ADDR"),
    (r':',                      "COLON"),
    (r',',                      "COMMA"),
    (r'[A-Za-z_][A-Za-z0-9_]*', "LABEL"),                                          
]


def do_lex(characters):
    characters.upper()
    tokens = []
    pos = 0
    n_line = 0
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                lexem = match.group(0)
                token = [lexem.replace('"', ''), tag]
                if tag:
                    # Removing # and @ for literals and addresses
                    if tag in ['LITERAL', 'ADDR']:
                        token[0] = token[0][1:]
                    tokens.append(token)
                    if tag == 'NLINE':
                        n_line += 1     
                break   
        if not match:
            print(f"Wrong character '{characters[pos]}' at {n_line+1} line")
            return(tokens)
            sys.exit(0)
        else:
            pos = match.end(0)
    if tokens[-1][1] != 'NLINE':
        tokens.append(['\n', 'NLINE'])
    return tokens


if __name__ == '__main__':
    with open('test.ass', 'r') as f:
        program = f.read()
    print(do_lex(program))      