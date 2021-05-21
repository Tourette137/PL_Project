import ply.yacc as yacc
from program_lex import tokens
import program_print as printer
import sys

# Production rules
def p_Program(p):
    "Program : Decls BeginInstrs Instrs EndInstrs"
    pass

# Declaration block
def p_Decls1(p):
    "Decls : Decls Decl"

def p_Decls2(p):
    "Decls : Decl"

def p_Decl(p):
    "Decl : INT IntVars ';'"

def p_IntVars1(p):
    "IntVars : IntVars ',' IntVar"

def p_IntVars2(p):
    "IntVars : IntVar"

def p_IntVar(p):
    "IntVar : VAR"
    
    name = p[1]

    if (name in p.parser.identifier_table):
        print(name, ": Variável já existente!")
        parser.success = False
    else:
        p.parser.identifier_table[name] = ['int', p.parser.var_offset, 1]
        p.parser.var_offset += 1
        printer.var('0')


# Instructions block
def p_BeginInstrs(p):
    "BeginInstrs : BEGIN_INSTRS"
    printer.begin_instrs()

def p_EndInstrs(p):
    "EndInstrs : END_INSTRS"
    printer.end_instrs()

def p_Instrs1(p):
    "Instrs : Instrs Instr"

def p_Instrs2(p):
    "Instrs : "

def p_Instr_Atrib(p):
    "Instr : VAR '=' Exp ';'"
    
    name = p[1]
    value = p[3]

    if (name in p.parser.identifier_table):
        offset = p.parser.identifier_table[name][1]
        printer.atrib(offset, value)
    else:
        print(name, ": Variável não declarada!")
        parser.success = False

def p_Exp_Termo_add(p):
    "Exp : Exp '+' Termo"
    p[0] = p[1] + p[3]

def p_Exp_Termo_sub(p):
    "Exp : Exp '-' Termo"
    p[0] = p[1] - p[3]

def p_Exp_Termo(p):
    "Exp : Termo"
    p[0] = p[1]

def p_Termo_Fator_mul(p):
    "Termo : Termo '*' Fator"
    p[0] = p[1] * p[3]

def p_Termo_Fator_div(p):
    "Termo : Termo '/' Fator"
    if (p[3] != 0):
        p[0] = p[1] / p[3]
    else:
        print('O was found as a factor, continuing with 0.')
        p[0] = 0

def p_Termo_Fator(p):
    "Termo : Fator"
    p[0] = p[1]

def p_Fator_id(p):
    "Fator : VAR"
    p[0] = 1

def p_Fator_num(p):
    "Fator : NUM"
    p[0] = int(p[1])

def p_Fator_Exp(p):
    "Fator : '(' Exp ')'"
    p[0] = p[1]


def p_error(p):
    print(f'Syntax Error: {p}')
    #parser.success = False


# Build parser
parser = yacc.yacc()
parser.identifier_table = {}
parser.var_offset = 0

# Identifier table
#  Name  |  Type  |  Offset  |  Size

# Inicialize printer
printer.begin()

# Read input and parse it
# Line by line
parser.success = True

for linha in sys.stdin:
    result = parser.parse(linha)
    # print(result)
    if parser.success == False:
        break

print(parser.identifier_table)
print(parser.var_offset)
