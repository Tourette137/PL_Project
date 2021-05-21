import ply.yacc as yacc
from program_lex import tokens
import program_print as printer
import sys

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
        printer.varDecl(0)


# Instructions block
def p_BeginInstrs(p):
    "BeginInstrs : BEGIN_INSTRS"
    printer.begin_instrs()

def p_EndInstrs(p):
    "EndInstrs : END_INSTRS"
    printer.end_instrs()

def p_Instrs(p):
    """
    Instrs : Instrs Instr
           | 
    """

def p_Instr_Atrib(p):
    "Instr : VAR '=' Exp ';'"
    
    name = p[1]

    if name in p.parser.identifier_table:
        offset = p.parser.identifier_table[name][1]
        printer.atrib(offset)
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False

def p_Instr_PrintNum(p):
    "Instr : WRITE '(' NUM ')' ';'"
    printer.write_num(p[3])

def p_Instr_PrintVar(p):
    "Instr : WRITE '(' VAR ')' ';'"

    name = p[3]

    if name in p.parser.identifier_table:
        offset = p.parser.identifier_table[name][1]
        printer.write_var(offset)
    else:
        print(name, ": Variável não declarada!")
        p.parser.success = False

def p_Instr_PrintStr(p):
    "Instr : WRITE '(' STR ')' ';'"
    printer.write_str(p[3])

def p_ExpVar(p):
    "Exp : VAR"
    if p[1] not in p.parser.identifier_table:
        print(p[1], ": Variável não declarada!")
        p.parser.success = False
    else:
        printer.pushVar(p[1])

def p_ExpNum(p):
    "Exp : NUM"
    printer.pushNum(p[1])

def p_ExpVarVar(p):
    "Exp : VAR OP VAR"
    var1 = p[1]
    var2 = p[3]
    if var1 not in p.parser.identifier_table:
        print(var1, ": Variável não declarada!")
        p.parser.success = False
    elif var2 not in p.parser.identifier_table:
        print(var2, ": Variável não declarada!")
        p.parser.success = False
    else:
        printer.pushVar(p.parser.identifier_table[var1][1])
        printer.pushVar(p.parser.identifier_table[var2][1])
        printer.operation(p[2])

def p_ExpVarNum(p):
    "Exp : VAR OP NUM"
    var = p[1]
    if var not in p.parser.identifier_table:
        print(var, ": Variável não declarada!")
        p.parser.success = False
    else:
        printer.pushVar(p.parser.identifier_table[var][1])
        printer.pushNum(p[3])
        printer.operation(p[2])

def p_ExpNumNum(p):
    "Exp : NUM OP NUM"
    printer.pushNum(p[1])
    printer.pushNum(p[3])
    printer.operation(p[2])

def p_ExpRead(p):
    "Exp : READ"
    printer.read()

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
        printer.clean()
        break


print(parser.identifier_table)
print(parser.var_offset)
