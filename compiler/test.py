from lexer import do_lex
from asm_parser import Parser
from compiler import Compiler
from assembler_lang import Assembler


with open('test.ass', 'r') as f:
    program = f.read()
    tokens = do_lex(program)
    parser = Parser(tokens)
    if (parser.is_valid_code()):
        valid_cmd_lines = parser.valid_cmd_lines
        print(valid_cmd_lines)
    
        compiler = Compiler(valid_cmd_lines)
        compiler.compile()
        program = compiler.compiled_cmds
        print(program)
        print(compiler.jumps)

        assembler = Assembler(program)
        assembler.execute_code()