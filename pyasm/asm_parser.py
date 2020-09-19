from sys import exit


class Parser:
    """
    A parser class, that's checking code according to grammar rules:

    lang -> expr*
    expr -> (NLINE | common | arifetic | logical | jump | label)

    common -> (pop | push | 'NOPE') NLINE
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

    reg -> "R[1-7]"
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
        self.valid_cmds = [] # List of valid cmds
        self.__n_line = 1 # Number of code line
        self.error_msg = ''

    def exception(self, expected):
        self.error_msg = f"\nParse error at line {self.__n_line}: " + \
            f"detected '{self.tokens[self.__pos][0]}', " + \
            f"but '{expected}' are expected!"
        print(self.error_msg)
    
    def __check_token_tag(self, tag):
        """
        Check tag of current token
        """
        if self.tokens[self.__pos][1] == tag:
            if tag == 'NLINE':
                self.__n_line += 1
                if self.__temp:
                    self.valid_cmds.append(self.__temp)
                self.__temp = []
            else:
                self.__temp.append(self.tokens[self.__pos])
            self.__pos += 1

            return True
        return False

    def is_valid_code(self):
        return self.__lang(), self.error_msg

    def __lang(self):
        """
        lang -> expr*
        """
        while(self.__pos < len(self.tokens)):
            if (not self.__expr()):
                self.exception("any expression")
                return False
        return True    

    def __expr(self):
        """
        expr -> (NLINE | common | arifetic | logical | jump | label)
        """
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

    def __common(self):
        """
        common -> (pop | push | 'NOPE') NLINE
        """
        if not (
            self.__pop() or
            self.__push() or 
            self.__check_token_tag('NOPE')
        ):
            return False
        if not self.__check_token_tag('NLINE'):
            self.exception('new line')
            return False
        return True  

    def __arifetic(self):
        """
        arifetic -> arif_op NLINE
        """
        if not (
            self.__arif_op()
        ):
            return False
        elif not self.__check_token_tag('NLINE'):
            self.exception('new line')
            return False
        return True  

    def __logical(self):
        """
        logical -> (log_op | comp_op | shift_op) NLINE
        """
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

    def __jump(self):
        """
        jump -> jmp_op (addr | LABEL) NLINE
        """
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
    
    def __label(self):
        """
        label -> LABEL COLON NLINE
        """
        if not self.__check_token_tag('LABEL'):
            return False
        if not self.__check_token_tag('COLON'):
            self.exception(':')
            return False
        if not self.__check_token_tag('NLINE'):
            self.exception('new line')
            return False
        return True 
  
    def __pop(self):
        """
        pop -> 'POP' (addr | reg)
        """
        if not self.__check_token_tag('POP'):
            return False
        if not (
            self.__check_token_tag('ADDR') or
            self.__check_token_tag('REG')
        ):
            self.exception('ADDRESS or REGISTER')
            return False
        return True       

    def __push(self):
        """
        push -> 'PUSH' ('ADDR' | 'LITERAL' | 'REG')
        """
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

    def __arif_op(self):
        """
        arif_op -> 'ADD' | 'SUB' | 'INC' | 'DEC'
        """
        if (
            self.__check_token_tag('ADD') or
            self.__check_token_tag('SUB') or
            self.__check_token_tag('INC') or
            self.__check_token_tag('DEC')
        ):
            return True
        return False

    def __log_op(self):
        """
        log_op -> 'AND' | 'OR' | 'XOR' | 'NOR' | 'NOT'
        """
        if (
            self.__check_token_tag('AND') or
            self.__check_token_tag('OR') or
            self.__check_token_tag('XOR') or
            self.__check_token_tag('NOR') or 
            self.__check_token_tag('NOT')
        ):
            return True
        return False       

    def __comp_op(self):
        """
        comp_op -> 'CMP'
        """
        if (
            self.__check_token_tag('CMP') 
        ):
            return True
        return False

    def __shift_op(self):
        """
        shift_op -> 'SHL' | 'SHR'
        """
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
