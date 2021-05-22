from src.atribs import *
from src.conds import *
from src.decls import *
from src.exps import *
from src.instrs import *

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
    "Instr : WRITE '(' ARR_OPEN Exp ARR_CLOSE ')' ';'"

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

def p_Instr_PrintMatVar(p):
    "Instr : WRITE '(' MATVAR ')' ';'"

    result = re.search(r'([a-z]+)\[(\d+)\]\[(\d+)\]', p[3])
    name = result.group(1)
    lines = int(result.group(2))
    cols = int(result.group(3))
    pos = lines * cols + cols

    if name in p.parser.identifier_table:
        offset = p.parser.identifier_table[name][1]

        # put array pointer on top of the stack
        p[0] = "\tpushgp\n"
        p[0] += "\tpushi " + str(offset) + "\n"
        p[0] += "\tpadd\n"
        
        # load value in the array
        p[0] += "\tload " + str(pos) + "\n"

        # send value to output
        p[0] += "\twritei\n"
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False
