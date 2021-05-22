import ply.yacc as yacc
from program_lex import tokens

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

# Declaration block
def p_Decls1(p):
    "Decls : IntDecls ArrDecls"
    p[0] = p[1] + p[2]

def p_IntDecls(p):
    "IntDecls : INT IntVars ';'"
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

def p_ArrDecls(p):
    "ArrDecls : ARR ArrVars ';'"
    p[0] = p[2]

def p_ArrVars1(p):
    "ArrVars : ArrVars ',' ArrVar"
    p[0] = p[1] + p[3]

def p_ArrVars2(p):
    "ArrVars : ArrVar"
    p[0] = p[1]

def p_ArrVar(p):
    "ArrVar : ARRVAR"

    result = re.search(r'([a-z]+)\[(\d+)\]', p[1])
    name = result.group(1)
    size = int(result.group(2))

    if name in p.parser.identifier_table:
        print(name, ": Variável já existente!")
        p.parser.success = False
    else:
        p.parser.identifier_table[name] = ['arr', p.parser.var_offset, size]
        p.parser.var_offset += size
        p[0] = "\tpushn " + str(size) + "\n"

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

def p_AtribArrVar(p):
    "Atrib : ARRVAR '=' Exp"

    result = re.search(r'([a-z]+)\[(\d+)\]', p[1])
    name = result.group(1)
    pos = int(result.group(2))

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

def p_Instr_PrintArrVar(p):
    "Instr : WRITE '(' ARRVAR ')' ';'"

    result = re.search(r'([a-z]+)\[(\d+)\]', p[3])
    name = result.group(1)
    pos = int(result.group(2))

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

def p_Fator_ArrVar(p):
    "Fator : ARRVAR"

    result = re.search(r'([a-z]+)\[(\d+)\]', p[1])
    name = result.group(1)
    pos = int(result.group(2))

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
parser.identifier_table = {}  # {'var' : [type, offset, size]}
parser.var_offset = 0
parser.if_count = 0
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
