from sys import exit


class Parser:
    """
    A parser class, that's checking code according to grammar rules:

    lang -> expr*
    expr -> (NLINE | common | arifetic | logical | jump | label)

    common -> (pop | push) NLINE
    arifetic -> arif_op NLINE
    logical -> (log_op | comp_op | shift_op) NLINE
    jump -> jmp_op (addr | LABEL) NLINE
    label -> LABEL COLON NLINE

    pop -> 'POP' (addr | reg)
    push -> 'PUSH' (addr | literal | reg)

    arif_op -> 'ADD' | 'SUB' | 'INC' | 'DEC'
    log_op -> 'AND' | 'OR' | 'XOR' | 'NOR' | 'NOT'
    comp_op -> 'CMP'
    shift_op -> 'SHL' | 'SHR'

    jmp_op -> 'JC' | 'JZ' | 'JP' | 'JO' | 'JS' | 'JMP'
        | 'NJC' | 'NJZ' | 'NJP' | 'NJO' | 'NJS'

    reg -> "R[1-7]*"
    literal -> "#[0-9A-F]+"
    addr -> "@[0-9A-F]+|@R[1-7]"
    NLINE -> "[\n]+"
    LABEL -> "[A-Za-z_][A-Za-z0-9_]*"
    COLON -> ":"
    """
    def __init__(self, tokens):
        self.tokens = tokens # List of tokens after lexer
        self.__pos = 0 # Current position in tokens
        self.__temp = [] # Temporary code lines for validation
        self.valid_cmd_lines = [] # List of valid cmd lines
        self.__n_line = 1 # Number of code line

    def exception(self, expected):
        print(f"\nParse error at line {self.__n_line}: " + \
            f"detected '{self.tokens[self.__pos][0]}', " + \
            f"but '{expected}' are expected!")
        exit(0)
    
    # Check tag of current token
    def __check_token_tag(self, tag):
        if self.tokens[self.__pos][1] == tag:
            if tag == 'NLINE':
                self.__n_line += 1
                if self.__temp:
                    self.valid_cmd_lines.append(self.__temp)
                self.__temp = []
            else:
                self.__temp.append(self.tokens[self.__pos])
            self.__pos += 1

            return True
        return False

    def is_valid_code(self):
        return self.__lang()

    # lang -> expr*
    def __lang(self):
        while(self.__pos < len(self.tokens)):
            if (not self.__expr()):
                self.exception("any expression")
                return False
        return True    

    # expr -> (common | arifetic | logical | jump) NLINE
    def __expr(self):
        if not (
            self.__check_token_tag('NLINE') or
            self.__common() or
            self.__arifetic() or
            self.__logical() or
            self.__jump() or
            self.__label()
        ):
            return False
        return True  

    # common -> mov | pop | push
    def __common(self):
        if not (
            self.__pop() or
            self.__push()
        ):
            return False
        if not self.__check_token_tag('NLINE'):
            self.exception('new line')
            return False
        return True  

    # arifetic -> arif_op
    def __arifetic(self):
        if not (
            self.__arif_op()
        ):
            return False
        elif not self.__check_token_tag('NLINE'):
            self.exception('new line')
            return False
        return True  

    # logical -> log_op | comp_op | shift_op
    def __logical(self):
        if not (
            self.__log_op() or
            self.__comp_op() or 
            self.__shift_op() 
        ):
            return False
        elif not self.__check_token_tag('NLINE'):
            self.exception('new line')
            return False
        return True  

    # jump -> jmp_op addr   
    def __jump(self):
        if not self.__jmp_op():
            return False
        if not (
            self.__check_token_tag('ADDR') or
            self.__check_token_tag('LABEL')
        ):
            self.exception('ADDRESS or LABEL')
            return False
        if not self.__check_token_tag('NLINE'):
            self.exception('new line')
            return False
        return True
    
    # label -> LABEL COMMA
    def __label(self):
        if not self.__check_token_tag('LABEL'):
            return False
        if not self.__check_token_tag('COLON'):
            self.exception(':')
            return False
        if not self.__check_token_tag('NLINE'):
            self.exception('new line')
            return False
        return True 

    # pop -> 'POP' (addr | reg)   
    def __pop(self):
        if not self.__check_token_tag('POP'):
            return False
        if not (
            self.__check_token_tag('ADDR') or
            self.__check_token_tag('REG')
        ):
            self.exception('ADDRESS or REGISTER')
            return False
        return True       

    # push -> 'PUSH' (literal | reg)
    def __push(self):
        if not self.__check_token_tag('PUSH'):
            return False
        if not (
            self.__check_token_tag('ADDR') or
            self.__check_token_tag('LITERAL') or
            self.__check_token_tag('REG')
        ):
            self.exception('ADDRESS, LITERAL or REGISTER')
            return False
        return True

    # arif_op -> 'ADD' | 'SUB'
    def __arif_op(self):
        if (
            self.__check_token_tag('ADD') or
            self.__check_token_tag('SUB') or
            self.__check_token_tag('INC') or
            self.__check_token_tag('DEC')
        ):
            return True
        return False

    # log_op -> 'AND' | 'OR' | 'XOR' | 'NOR' | 'NOT'
    def __log_op(self):
        if (
            self.__check_token_tag('AND') or
            self.__check_token_tag('OR') or
            self.__check_token_tag('XOR') or
            self.__check_token_tag('NOR') or 
            self.__check_token_tag('NOT')
        ):
            return True
        return False       

    # comp_op -> 'CMP'
    def __comp_op(self):
        if (
            self.__check_token_tag('CMP') 
        ):
            return True
        return False

    # shift_op -> 'SHL' | 'SHR'     
    def __shift_op(self):
        if (
            self.__check_token_tag('SHL') or
            self.__check_token_tag('SHR')
        ):
            return True
        return False

    def __jmp_op(self):
        """
        jmp_op -> 'JC' | 'JZ' | 'JP' | 'JO' | 'JS' | 'JMP'
            | 'NJC' | 'NJZ' | 'NJP' | 'NJO' | 'NJS'
        """
        if not (
            self.__check_token_tag('JC') or
            self.__check_token_tag('JZ') or
            self.__check_token_tag('JS') or
            self.__check_token_tag('JP') or
            self.__check_token_tag('JO') or
            self.__check_token_tag('NJC') or
            self.__check_token_tag('NJZ') or
            self.__check_token_tag('NJS') or
            self.__check_token_tag('NJP') or
            self.__check_token_tag('NJO') or
            self.__check_token_tag('JMP')
        ):
            return False
        return True
