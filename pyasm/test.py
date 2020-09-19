from pyasm.lexer import do_lex
from pyasm.asm_parser import Parser
from pyasm.compiler import Compiler
from pyasm.assembler_lang import Assembler


with open('test.ass', 'r') as f:
    program = f.read()
    tokens = do_lex(program)
    parser = Parser(tokens)
    parse_result = parser.is_valid_code()
    if parse_result[0]:
        compiler = Compiler( parser.valid_cmds )
        compiler.compile()

    assembler = Assembler(program)
    assembler.execute_all_code()