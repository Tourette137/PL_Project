from typing import Type
import ply.yacc as yacc
from program_lex import tokens

from atribs import *
from conds import *
from decls import *
from exps import *
from instrs import *
from ios import *

import sys
import os

# Production rules
def p_Program(p):
    "Program : Decls BeginInstrs Instrs EndInstrs"
    f.write(p[1])
    f.write(p[2])
    f.write(p[3])
    f.write(p[4])

def p_error(p):
    print(f'Syntax Error: {p}')
    parser.success = False


# Build parser
parser = yacc.yacc(start='Program', outputdir='out')
parser.identifier_table = {}  # {'var' : [type, offset, size]}
parser.var_offset = 0
parser.if_count = 0
parser.repeat_count = 0
parser.while_count = 0
parser.for_count = 0

# Read input and parse it
# Line by line
parser.success = True

if len(sys.argv) > 1:
    input = open(sys.argv[1], "r")
    content = input.read()
    input.close

    file_name = sys.argv[1].split(".", 1)[0] + ".vm"
else:
    content = sys.stdin.read()
    
    file_name = "output.vm"


f = open(file_name, "w")
try:
    parser.parse(content)
except SyntaxError as e1:
    print("Syntax Error. [Verifique possíveis erros na escrita do código]\n")
except TypeError as e2:
    print("Syntax Error. [Verifique possíveis erros na escrita do código]\n")
f.close

if not parser.success:
    os.remove(file_name)


#print(parser.identifier_table)
#print(parser.var_offset)
#print(parser.if_count)
