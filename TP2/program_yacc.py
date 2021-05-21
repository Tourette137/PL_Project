import ply.yacc as yacc
from program_lex import tokens
import sys
import os

# Production rules
def p_Program(p):
    """
    Program : Decls
            | BeginInstrs
            | Instrs
            | EndInstrs
    """

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

    if name in p.parser.identifier_table:
        print(name, ": Variável já existente!")
        p.parser.success = False
    else:
        p.parser.identifier_table[name] = ['int', p.parser.var_offset, 1]
        p.parser.var_offset += 1
        f.write("\tpushi 0\n")


# Instructions block
def p_BeginInstrs(p):
    "BeginInstrs : BEGIN_INSTRS"
    f.write("start\n")

def p_EndInstrs(p):
    "EndInstrs : END_INSTRS"
    f.write("stop\n")

def p_Instrs1(p):
    "Instrs : Instrs Instr ';'"
    f.write(p[1] + p[2])

def p_Instrs2(p):
    "Instrs : Instrs IfStat"
    f.write(p[1] + p[2])

def p_Instrs3(p):
    "Instrs : "
    p[0] = ""

def p_IfStat(p):
    "IfStat : IF '(' Cond ')' '{' Instrs '}'"

    p[0] = p[3]
    p[0] += "\tjz end_if" + str(p.parser.if_count) + "\n"

    p[0] += p[6]
    p[0] += "end_if" + p.parser.if_count + "\n"

    p.parser.if_count += 1

def p_Cond(p):
    "Cond : Exp OPCOMP Exp"

    p[0] = p[1]
    p[0] += p[3]

    if p[2] == '==':
        p[0] += "\tequal\n"
    elif p[2] == '>':
        p[0] += "\tsup\n"
    elif p[2] == '>=':
        p[0] += "\tsupeq\n"
    elif p[2] == '<':
        p[0] += "\tinf\n"
    elif p[2] == '<=':
        p[0] += "\tinfeq\n"
        

def p_Instr_Atrib(p):
    "Instr : VAR '=' Exp"
    
    name = p[1]

    if name in p.parser.identifier_table:
        p[0] = p[3]

        offset = p.parser.identifier_table[name][1]
        p[0] += "\tstoreg " + str(offset) + "\n"
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False

def p_Instr_PrintNum(p):
    "Instr : WRITE '(' NUM ')'"
    p[0] = "\tpushi " + str(p[3]) + "\n"
    p[0] += "\twritei\n"

def p_Instr_PrintVar(p):
    "Instr : WRITE '(' VAR ')'"

    name = p[3]

    if name in p.parser.identifier_table:
        offset = p.parser.identifier_table[name][1]
        p[0] = "\tpushg " + str(offset) + "\n"
        p[0] += "\twritei\n"
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False

def p_Instr_PrintStr(p):
    "Instr : WRITE '(' STR ')'"
    p[0] = "\tpushs " + p[3] + "\n"
    p[0] += "\twrites\n"

def p_ExpVar(p):
    "Exp : VAR"
    if p[1] not in p.parser.identifier_table:
        print(p[1], ": Variável não declarada!")
        p.parser.success = False
    else:
        p[0] = "\tpushg " + str(p[1]) + "\n"

def p_ExpNum(p):
    "Exp : NUM"
    p[0] = "\tpushi " + str(p[1]) + "\n"

def p_ExpVarVar(p):
    "Exp : VAR OPARIT VAR"

    var1 = p[1]
    var2 = p[3]

    if var1 not in p.parser.identifier_table:
        print(var1, ": Variável não declarada!")
        p.parser.success = False
    elif var2 not in p.parser.identifier_table:
        print(var2, ": Variável não declarada!")
        p.parser.success = False
    else:
        offset1 = p.parser.identifier_table[var1][1]
        offset2 = p.parser.identifier_table[var2][1]
        p[0] = "\tpushg " + str(offset1) + "\n"
        p[0] += "\tpushg " + str(offset2) + "\n"
        
        if p[2] == '+':
            p[0] += "\tadd\n"
        elif p[2] == '-':
            p[0] += "\tsub\n"
        elif p[2] == '*':
            p[0] += "\tmul\n"
        elif p[2] == '/':
            p[0] += "\tdiv\n"

def p_ExpVarNum(p):
    "Exp : VAR OPARIT NUM"
    var = p[1]
    if var not in p.parser.identifier_table:
        print(var, ": Variável não declarada!")
        p.parser.success = False
    else:
        offset = p.parser.identifier_table[var][1]
        p[0] = "\tpushg " + str(offset) + "\n"
        p[0] += "\tpushi " + str(p[3]) + "\n"

        if p[2] == '+':
            p[0] += "\tadd\n"
        elif p[2] == '-':
            p[0] += "\tsub\n"
        elif p[2] == '*':
            p[0] += "\tmul\n"
        elif p[2] == '/':
            p[0] += "\tdiv\n"

def p_ExpNumNum(p):
    "Exp : NUM OPARIT NUM"

    p[0] = "\tpushi " + str(p[1]) + "\n"
    p[0] += "\tpushi " + str(p[3]) + "\n"

    if p[2] == '+':
        p[0] += "\tadd\n"
    elif p[2] == '-':
        p[0] += "\tsub\n"
    elif p[2] == '*':
        p[0] += "\tmul\n"
    elif p[2] == '/':
        p[0] += "\tdiv\n"

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

# Identifier table
#  Name  |  Type  |  Offset  |  Size


# Read input and parse it
# Line by line
parser.success = True
file_name = "output.vm"
f = open(file_name, "w")

for linha in sys.stdin:
    result = parser.parse(linha)
    # print(result)
    if parser.success == False:
        os.remove(file_name)
        break


print(parser.identifier_table)
print(parser.var_offset)
