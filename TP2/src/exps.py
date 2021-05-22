from src.atribs import *
from src.conds import *
from src.decls import *
from src.instrs import *
from src.ios import *

import re

def p_Exp_Termo_add(p):
    "Exp : Exp '+' Termo"
    p[0] = p[1] + p[3] + "\tadd\n"

def p_Exp_Termo_sub(p):
    "Exp : Exp '-' Termo"
    p[0] = p[1] + p[3] + "\tsub\n"

def p_Exp_Termo(p):
    "Exp : Termo"
    p[0] = p[1]

def p_Termo_Fator_mul(p):
    "Termo : Termo '*' Fator"
    p[0] = p[1] + p[3] + "\tmul\n"

def p_Termo_Fator_div(p):
    "Termo : Termo '/' Fator"
    if (p[3] != 0):
        p[0] = p[1] + p[3] + "\tdiv\n"
    else:
        print("0 encontrado como divisor. Operação impossível")
        p.parser.success = False

def p_Termo_Fator_mod(p):
    "Termo : Termo '%' Fator"
    if (p[3] != 0):
        p[0] = p[1] + p[3] + "\tmod\n"
    else:
        print("0 encontrado como divisor. Operação impossível")
        p.parser.success = False


def p_Termo_Fator(p):
    "Termo : Fator"
    p[0] = p[1]

def p_Fator_num(p):
    "Fator : NUM"
    p[0] = "\tpushi " + str(p[1]) + "\n"

def p_Fator_Exp(p):
    "Fator : '(' Exp ')'"
    p[0] = p[2]

def p_Fator_Var(p):
    "Fator : VAR"
    var = p[1]
    if var not in p.parser.identifier_table:
        print(var, ": Variável não declarada!")
        p.parser.success = False
    else:
        offset = p.parser.identifier_table[var][1]
        p[0] = "\tpushg " + str(offset) + "\n"

def p_Fator_Array(p):
    "Fator : ARR_OPEN Exp ARR_CLOSE"

    result = re.search(r'([a-z]+)\[', p[1])
    name = result.group(1)

    if name in p.parser.identifier_table:
        offset = p.parser.identifier_table[name][1]

        # put array pointer on top of the stack
        p[0] = "\tpushgp\n"
        p[0] += "\tpushi " + str(offset) + "\n"
        p[0] += "\tpadd\n"

        # put Exp value on top of the stack
        p[0] += p[2]
        
        # load value in the array
        p[0] += "\tloadn\n"
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False

def p_Fator_MatVar(p):
    "Fator : MATVAR"

    result = re.search(r'([a-z]+)\[(\d+)\]\[(\d+)\]', p[1])
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
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False
