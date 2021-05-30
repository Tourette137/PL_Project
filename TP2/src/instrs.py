from atribs import *
from conds import *
from decls import *
from exps import *
from ios import *

def p_BeginInstrs(p):
    "BeginInstrs : BEGIN_INSTRS"
    p[0] = "start\n"

def p_EndInstrs(p):
    "EndInstrs : END_INSTRS"
    p[0] = "stop\n"

def p_Instrs(p):
    "Instrs : Instrs Instr"
    p[0] = p[1] + p[2]

def p_Instrs_Empty(p):
    "Instrs : "
    p[0] = ""

def p_Instr_Atrib(p):
    "Instr : Atrib ';'"
    p[0] = p[1]

def p_Instr_IfStat(p):
    "Instr : IF '(' Conds ')' '{' Instrs '}'"

    p[0] = p[3]
    p[0] += "\tjz endif" + str(p.parser.if_count) + "\n"

    p[0] += p[6]
    p[0] += "endif" + str(p.parser.if_count) + ":\n"

    p.parser.if_count += 1

def p_Instr_IfElseStat(p):
    "Instr : IF '(' Conds ')' '{' Instrs '}' ELSE '{' Instrs '}'"

    count = str(p.parser.if_count)

    p[0] = p[3]
    p[0] += "\tjz elseif" + count + "\n"

    p[0] += p[6]
    p[0] += "\tjump endif" + count + "\n"
    p[0] += "elseif" + count + ":\n"

    p[0] += p[10]
    p[0] += "endif" + count + ":\n"

    p.parser.if_count += 1

def p_Instr_RepeatStat(p):
    "Instr : REPEAT '{' Instrs '}' UNTIL '(' Conds ')'"

    count = str(p.parser.repeat_count)

    p[0] = "repeatstat" + count + ":\n"
    p[0] += p[3]
    p[0] += p[7]
    p[0] += "\tjz repeatstat" + count + "\n"

    p.parser.repeat_count += 1

def p_Instr_WhileStat(p):
    "Instr : WHILE '(' Conds ')' DO '{' Instrs '}'"

    count = str(p.parser.for_count)

    p[0] = "whilestat" + count + ":\n"
    p[0] +=  p[3]
    p[0] += "\tjz endwhilestat" + count + "\n"

    p[0] += p[7]
    p[0] += "jump whilestat" + count + ":\n"
    p[0] += "endwhilestat" + count + ":\n"

    p.parser.while_count += 1

def p_Instr_ForStat(p):
    "Instr : FOR '(' Atribs ';' Conds ';' Atribs ')' '{' Instrs '}'"

    count = str(p.parser.for_count)

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
