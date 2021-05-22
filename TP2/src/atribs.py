from src.conds import *
from src.decls import *
from src.exps import *
from src.instrs import *
from src.ios import *

import re

def p_Atribs1(p):
    "Atribs : Atribs ',' Atrib"
    p[0] = p[1] + p[3]

def p_Atribs2(p):
    "Atribs : Atrib"
    p[0] = p[1]

def p_Atribs3(p):
    "Atribs : "
    p[0] = ""

def p_AtribVar(p):
    "Atrib : VAR '=' Exp"

    name = p[1]

    if name in p.parser.identifier_table:
        p[0] = p[3]

        offset = p.parser.identifier_table[name][1]
        p[0] += "\tstoreg " + str(offset) + "\n"
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False

def p_AtribArray(p):
    "Atrib : ARR_OPEN Exp ARR_CLOSE '=' Exp"

    result = re.search(r'([a-z]+)\[', p[1])
    name = result.group(1)

    if name in p.parser.identifier_table:
        offset = p.parser.identifier_table[name][1]
        
        # put array pointer on top of the stack
        p[0] = "\tpushgp\n"
        p[0] += "\tpushi " + str(offset) + "\n"
        p[0] += "\tpadd\n"

        # put Exp(array pos) on top of the stack
        p[0] += p[2]
        
        # put Exp value on top of the stack
        p[0] += p[5]

        # store Exp value in array
        p[0] += "\tstoren\n"
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False

def p_AtribMatVar(p):
    "Atrib : MATVAR '=' Exp"

    result = re.search(r'([a-z]+)\[(\d+)\]\[(\d+)\]', p[1])
    name = result.group(1)
    lines = int(result.group(2))
    cols = int(result.group(3))
    pos = lines * cols + cols

    if name in p.parser.identifier_table:
        offset = p.parser.identifier_table[name][1]
        
        p[0] = p[3]
        # expression value is on top of the stack

        # get array pointer
        p[0] += "\tpushgp\n"
        p[0] += "\tpushi " + str(offset) + "\n"
        p[0] += "\tpadd\n"
        # swap values so we can match STOREN command sintax
        p[0] += "\tswap\n"
        # store value in array
        p[0] += "\tstore " + str(pos) + "\n"
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False
