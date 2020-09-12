from lexer import do_lex
from asm_parser import Parser
from compiler import Compiler


with open('test.ass', 'r') as f:
    program = f.read()
    tokens = do_lex(program)
    parser = Parser(tokens)
    if (parser.is_valid_code()):
        valid_cmd_lines = parser.valid_cmd_lines
        print(valid_cmd_lines)
    
        compiler = Compiler(valid_cmd_lines)
        compiler.compile()
        print(compiler.compiled_cmds)
        print(compiler.jumps)