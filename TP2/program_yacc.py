import ply.yacc as yacc
from program_lex import tokens

from src.atribs import *
from src.conds import *
from src.decls import *
from src.exps import *
from src.instrs import *
from src.ios import *

import sys
import os
import re

# Production rules
def p_Program(p):
    "Program : Decls BeginInstrs Instrs EndInstrs"
    f.write(p[1])
    f.write(p[2])
    f.write(p[3])
    f.write(p[4])

def p_error(p):
    print(f'Syntax Error: {p}')
    #parser.success = False


# Build parser
parser = yacc.yacc(start='Program')
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
parser.parse(content)

if not parser.success:
    os.remove(file_name)


#print(parser.identifier_table)
#print(parser.var_offset)
#print(parser.if_count)
