from conds import *
from decls import *
from exps import *
from instrs import *
from ios import *

import re

def p_Atribs(p):
    "Atribs : Atribs ',' Atrib"
    p[0] = p[1] + p[3]

def p_Atribs_Atrib(p):
    "Atribs : Atrib"
    p[0] = p[1]

def p_Atribs_Empty(p):
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
    "Atrib : ARR_OPEN Exp ']' '=' Exp"

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

def p_AtribMatrix(p):
    "Atrib : ARR_OPEN Exp MAT_INT Exp ']' '=' Exp"

    result = re.search(r'([a-z]+)\[', p[1])
    name = result.group(1)

    if name in p.parser.identifier_table:
        offset = p.parser.identifier_table[name][1]
        cols = p.parser.identifier_table[name][3]
        
        # put array pointer on top of the stack
        p[0] = "\tpushgp\n"
        p[0] += "\tpushi " + str(offset) + "\n"
        p[0] += "\tpadd\n"

        # put n(pos in array) on top of the stack
        p[0] += p[2]
        p[0] += "\tpushi " + str(cols) + "\n"
        p[0] += "\tmul"

        p[0] += p[4]
        p[0] += "\tadd"
                
        # put Exp value on top of the stack
        p[0] += p[7]

        # store Exp value in array
        p[0] += "\tstoren\n"
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False
