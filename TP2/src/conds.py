from src.atribs import *
from src.decls import *
from src.exps import *
from src.instrs import *
from src.ios import *

def p_Conds1(p):
    "Conds : Conds OPLOGIC Condz"

    p[0] = p[1]
    p[0] += p[3]

    if p[2] == 'AND':
        p[0] += "\tadd\n"
        p[0] += "\tpushi 2\n"
        p[0] += "\tequal\n"
    else:
        p[0] += "\tadd\n"
        p[0] += "\tpushi 0\n"
        p[0] += "\tsup\n"

def p_Conds2(p):
    "Conds : Condz"
    p[0] = p[1]

def p_Condz1(p):
    "Condz : '(' Conds ')'"
    p[0] = p[2]

def p_Condz2(p):
    "Condz : Cond"
    p[0] = p[1]

def p_Cond(p):
    "Cond : Exp OPCOMP Exp"

    p[0] = p[1]
    p[0] += p[3]

    if p[2] == '==':
        p[0] += "\tequal\n"
    elif p[2] == '!=':
        p[0] += "\tequal\n"
        p[0] += "\tnot\n"
    elif p[2] == '>':
        p[0] += "\tsup\n"
    elif p[2] == '>=':
        p[0] += "\tsupeq\n"
    elif p[2] == '<':
        p[0] += "\tinf\n"
    elif p[2] == '<=':
        p[0] += "\tinfeq\n"
