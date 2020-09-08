import re
import sys


token_exprs = [
    (r'[ \t\n]+',                  None), # Spaces, tabs, new lines
    (r';[^\n]*',                   None), # Comment 

    (r'PUSH',                    "PUSH"),
    (r'POP',                      "POP"),

    (r'MOV',                      "MOV"),
    (r'R[1-7]+',                  "REG"), # One of registers R1-R7

    (r'CMP',                      "CMP"), 

    (r'JMP',                      "JMP"),
    (r'JZ',                        "JZ"),
    (r'JC',                        "JC"),

    (r'ADD',                      "ADD"),
    (r'SUB',                      "SUB"),
 
    (r'SHL',                      "SHL"), # Shift left
    (r'SHR',                      "SHR"), # Shift right
 
    (r'AND',                      "AND"),
    (r'OR',                        "OR"),
    (r'NOR',                      "NOR"),
    (r'XOR',                      "XOR"),     
    (r'NOT',                      "NOT"),

    (r'#[0-9A-F]+',           "LITERAL"),
    (r'[0-9A-F]+',            "ADDRESS"),
    (r':',                      "COLON"),
    (r',',                      "COMMA"),
    (r'[A-Za-z_][A-Za-z0-9_]*', "LABEL"),                                          
]


def do_lex(characters):
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
                if '\n' in lexem:
                    n_line += 1
                if tag:
                    token = (lexem.replace('"',''), tag)
                    tokens.append(token)
                break
        if not match:
            print(f"Wrong character '{characters[pos]}' at {n_line+1} line")
            return(tokens)
            sys.exit(0)
        else:
            pos = match.end(0)
    return tokens


if __name__ == '__main__':
    with open('test.ass', 'r') as f:
        program = f.read()
    print(do_lex(program))      