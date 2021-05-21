import ply.yacc as yacc
from program_lex import tokens
import sys
import os

# Production rules
def p_Program(p):
    "Program : Decls BeginInstrs Instrs EndInstrs"
    f.write(p[1])
    f.write(p[2])
    f.write(p[3])
    f.write(p[4])

# Declaration block
def p_Decls1(p):
    "Decls : Decls Decl"
    p[0] = p[1] + p[2]

def p_Decls2(p):
    "Decls : Decl"
    p[0] = p[1]

def p_Decl(p):
    "Decl : INT IntVars ';'"
    p[0] = p[2]

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
        p.parser.identifier_table[name] = ['int', p.parser.var_offset, 1]
        p.parser.var_offset += 1
        p[0] = "\tpushi 0\n"

def p_IntVar2(p):
    "IntVar : VAR '=' NUM"
    
    name = p[1]

    if name in p.parser.identifier_table:
        print(name, ": Variável já existente!")
        p.parser.success = False
    else:
        p.parser.identifier_table[name] = ['int', p.parser.var_offset, 1]
        p.parser.var_offset += 1
        p[0] = "\tpushi " + p[3] + "\n"

# Instructions block
def p_BeginInstrs(p):
    "BeginInstrs : BEGIN_INSTRS"
    p[0] = "start\n"

def p_EndInstrs(p):
    "EndInstrs : END_INSTRS"
    p[0] = "stop\n"

def p_Instrs1(p):
    "Instrs : Instrs Instr"
    p[0] = p[1] + p[2]

def p_Instrs2(p):
    "Instrs : "
    p[0] = ""

def p_Instr_IfStat(p):
    "Instr : IF '(' Conds ')' '{' Instrs '}'"

    p[0] = p[3]
    p[0] += "\tjz endif" + str(p.parser.if_count) + "\n"

    p[0] += p[6]
    p[0] += "endif" + str(p.parser.if_count) + ":\n"

    p.parser.if_count += 1

def p_Instr_IfElseStat(p):
    "Instr : IF '(' Conds ')' '{' Instrs '}' ELSE '{' Instrs '}'"

    count = str(parser.if_count)

    p[0] = p[3]
    p[0] += "\tjz elseif" + count + "\n"

    p[0] += p[6]
    p[0] += "\tjump endif" + count + "\n"
    p[0] += "elseif" + count + ":\n"

    p[0] += p[10]
    p[0] += "endif" + count + ":\n"

    p.parser.if_count += 1


def p_Instr_ForStat(p):
    "Instr : FOR '(' Atribs ';' Conds ';' Atribs ')' '{' Instrs '}'"

    count = str(parser.for_count)

    p[0] =  p[3]
    p[0] += "jump forcond" + count + "\n"
    p[0] += "forstat" + count + ":\n"

    p[0] += p[10]
    p[0] += p[7]
    p[0] += "forcond" + count + ":\n"
    p[0] += p[5]
    p[0] += "\tnot\n"
    p[0] += "\tjz forstat" + count + "\n"

    p.parser.for_count += 1

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

def p_Atribs1(p):
    "Atribs : Atribs ',' Atrib"
    p[0] = p[1] + p[3]

def p_Atribs2(p):
    "Atribs : Atrib"
    p[0] = p[1]

def p_Atribs3(p):
    "Atribs : "
    p[0] = ""

def p_Atrib(p):
    "Atrib : VAR '=' Exp"

    name = p[1]

    if name in p.parser.identifier_table:
        p[0] = p[3]

        offset = p.parser.identifier_table[name][1]
        p[0] += "\tstoreg " + str(offset) + "\n"
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False


def p_Instr_Atrib(p):
    "Instr : Atrib ';'"
    p[0] = p[1]


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

def p_Instr_PrintStr(p):
    "Instr : WRITE '(' STR ')' ';'"
    p[0] = "\tpushs " + p[3] + "\n"
    p[0] += "\twrites\n"

def p_Exp_Termo_add(p):
    "Exp : Exp '+' Termo"
    p[0] = p[1] + p[3] + "\tadd\n"

def p_Exp_Termo_sub(p):
    "Exp : Exp '-' Termo"
    p[0] = p[1] - p[3] + "\tsub\n"

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
        parser.success = False

def p_Termo_Fator(p):
    "Termo : Fator"
    p[0] = p[1]

def p_Fator_Var(p):
    "Fator : VAR"
    var = p[1]
    if var not in p.parser.identifier_table:
        print(var, ": Variável não declarada!")
        p.parser.success = False
    else:
        offset = p.parser.identifier_table[var][1]
        p[0] = "\tpushg " + str(offset) + "\n"

def p_Fator_num(p):
    "Fator : NUM"
    p[0] = "\tpushi " + str(p[1]) + "\n"

def p_Fator_Exp(p):
    "Fator : '(' Exp ')'"
    p[0] = p[2]

def p_ExpRead(p):
    "Exp : READ"
    p[0] = "\tread\n"
    p[0] += "\tatoi\n"

def p_error(p):
    print(f'Syntax Error: {p}')
    #parser.success = False


# Build parser
parser = yacc.yacc()
parser.identifier_table = {}
parser.var_offset = 0
parser.if_count = 0
parser.for_count = 0

# Identifier table
#  Name  |  Type  |  Offset  |  Size


# Read input and parse it
# Line by line
parser.success = True
file_name = "output.vm"
f = open(file_name, "w")


content = sys.stdin.read()
parser.parse(content)

if not parser.success:
    os.remove(file_name)


#print(parser.identifier_table)
#print(parser.var_offset)
#print(parser.if_count)
