from atribs import *
from conds import *
from decls import *
from exps import *
from instrs import *

import re

def p_ExpRead(p):
    "Exp : READ"
    p[0] = "\tread\n"
    p[0] += "\tatoi\n"

def p_Instr_PrintStr(p):
    "Instr : WRITE '(' STR ')' ';'"
    p[0] = "\tpushs " + p[3] + "\n"
    p[0] += "\twrites\n"

def p_Instr_PrintNum(p):
    "Instr : WRITE '(' NUM ')' ';'"
    p[0] = "\tpushi " + str(p[3]) + "\n"
    p[0] += "\twritei\n"

def p_Instr_PrintVar(p):
    "Instr : WRITE '(' VAR ')' ';'"

    name = p[3]

    if name in p.parser.identifier_table:
        offset = p.parser.identifier_table[name][1]
        p[0] = "\tpushg " + str(offset) + "\n"
        p[0] += "\twritei\n"
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False

def p_Instr_PrintArray(p):
    "Instr : WRITE '(' ARR_OPEN Exp ']' ')' ';'"

    result = re.search(r'([a-z]+)\[', p[3])
    name = result.group(1)

    if name in p.parser.identifier_table:
        offset = p.parser.identifier_table[name][1]

        # put array pointer on top of the stack
        p[0] = "\tpushgp\n"
        p[0] += "\tpushi " + str(offset) + "\n"
        p[0] += "\tpadd\n"

        # put Exp value on top of the stack
        p[0] += p[4]
        
        # load value in the array
        p[0] += "\tloadn\n"

        # send value to output
        p[0] += "\twritei\n"
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False

def p_Instr_PrintMatrix(p):
    "Instr : WRITE '(' ARR_OPEN Exp MAT_INT Exp ']' ')' ';'"

    result = re.search(r'([a-z]+)\[', p[3])
    name = result.group(1)

    if name in p.parser.identifier_table:
        offset = p.parser.identifier_table[name][1]
        cols = p.parser.identifier_table[name][3]

        # put array pointer on top of the stack
        p[0] = "\tpushgp\n"
        p[0] += "\tpushi " + str(offset) + "\n"
        p[0] += "\tpadd\n"

        # put n(pos in array) on top of the stack
        p[0] += p[4]
        p[0] += "\tpushi " + str(cols) + "\n"
        p[0] += "\tmul"

        p[0] += p[6]
        p[0] += "\tadd"
        
        # load value in the array
        p[0] += "\tloadn\n"

        # send value to output
        p[0] += "\twritei\n"
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False
