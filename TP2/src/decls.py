from atribs import *
from conds import *
from exps import *
from instrs import *
from ios import *

import re

def p_Decls1(p):
    "Decls : IntDecls ArrayDecls"
    p[0] = p[1] + p[2]

def p_IntDecls1(p):
    "IntDecls : INT IntVars ';'"
    p[0] = p[2]

def p_IntDecls2(p):
    "IntDecls : "
    p[0] = ""

def p_IntVars1(p):
    "IntVars : IntVars ',' IntVar"
    p[0] = p[1] + p[3]

def p_IntVars2(p):
    "IntVars : IntVar"
    p[0] = p[1]

def p_IntVar1(p):
    "IntVar : VAR"
    
    name = p[1]

    if name in p.parser.identifier_table:
        print(name, ": Variável já existente!")
        p.parser.success = False
    else:
        p.parser.identifier_table[name] = ['int', p.parser.var_offset]
        p.parser.var_offset += 1
        p[0] = "\tpushi 0\n"

def p_IntVar2(p):
    "IntVar : VAR '=' NUM"
    
    name = p[1]

    if name in p.parser.identifier_table:
        print(name, ": Variável já existente!")
        p.parser.success = False
    else:
        p.parser.identifier_table[name] = ['int', p.parser.var_offset]
        p.parser.var_offset += 1
        p[0] = "\tpushi " + p[3] + "\n"

def p_ArrayDecls1(p):
    "ArrayDecls : ARRAY Arrays ';'"
    p[0] = p[2]

def p_ArrayDecls2(p):
    "ArrayDecls : "
    p[0] = ""

def p_Arrays1(p):
    "Arrays : Arrays ',' Array"
    p[0] = p[1] + p[3]

def p_Arrays2(p):
    "Arrays : Array"
    p[0] = p[1]

def p_Arrays3(p):
    "Arrays : Arrays ',' Matrix"
    p[0] = p[1] + p[3]

def p_Arrays4(p):
    "Arrays : Matrix"
    p[0] = p[1]

def p_Array(p):
    "Array : ARR_OPEN NUM ']'"

    result1 = re.search(r'([a-z]+)\[', p[1])
    name = result1.group(1)
    size = int(p[2])

    if name in p.parser.identifier_table:
        print(name, ": Variável já existente!")
        p.parser.success = False
    else:
        p.parser.identifier_table[name] = ['arr', p.parser.var_offset, size]
        p.parser.var_offset += size
        p[0] = "\tpushn " + str(size) + "\n"

def p_Matrix(p):
    "Matrix : ARR_OPEN NUM MAT_INT NUM ']'"

    result = re.search(r'([a-z]+)\[', p[1])
    name = result.group(1)
    lines = int(p[2])
    cols = int(p[4])

    if name in p.parser.identifier_table:
        print(name, ": Variável já existente!")
        p.parser.success = False
    else:
        p.parser.identifier_table[name] = ['mat', p.parser.var_offset, lines, cols]
        size = lines * cols
        p.parser.var_offset += size
        p[0] = "\tpushn " + str(size) + "\n"
