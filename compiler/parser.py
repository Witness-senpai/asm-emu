from sys import exit

from lexer import do_lex

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens # List of tokens after lexer
        self.__pos = 0 # Current position in tokens
        self.__temp = [] # Temporary code lines for validation
        self.pool = [] # Pool of valid tokens as list of code lines
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
                    self.pool.append(self.__temp)
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
            self.__mov() or
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

    # mov -> 'MOV' (addr | reg) (addr | reg | literal)   
    def __mov(self):
        if not self.__check_token_tag('MOV'):
            return False
        if not (
            self.__check_token_tag('ADDR') or
            self.__check_token_tag('REG')
        ):
            self.exception('ADDRESS OR REGISTER')
            return False
        if not (
            self.__check_token_tag('ADDR') or
            self.__check_token_tag('REG') or 
            self.__check_token_tag('LITERAL')
        ):
            self.exception('ADDRESS, REGISTER OR LITERAL')
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
            self.__check_token_tag('SUB')
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

    # jmp_op -> 'JC' | 'JZ' | 'JMP'
    def __jmp_op(self):
        if not (
            self.__check_token_tag('JC') or
            self.__check_token_tag('JZ') or
            self.__check_token_tag('JMP')
        ):
            return False
        return True

if __name__ == '__main__':
    with open('test.ass', 'r') as f:
        program = f.read()
    tokens = do_lex(program)

    parser = Parser(tokens)
    if (parser.is_valid_code()):
        print(parser.pool)
        