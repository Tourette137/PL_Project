import ply.lex as lex
import sys
tokens = ['INT', 'VAR', 'NUM', 'BEGIN_INSTRS', 'END_INSTRS', 'READ', 'WRITE', 'STR',
    'IF', 'ELSE', 'FOR', 'OPCOMP']
literals = [',', '=', ';', '+', '-', '*', '/', '(', ')', '"', '{', '}']

def t_INT(t):
    r'INT'
    return t

def t_READ(t):
    r'read\(\)'
    return t

def t_WRITE(t):
    r'write'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_FOR(t):
    r'for'
    return t

def t_BEGIN_INSTRS(t):
    r'BEGIN'
    return t

def t_END_INSTRS(t):
    r'END\.'
    return t

def t_OPCOMP(t):
    r'(==|!=|>|>=|<|<=)'
    return t

def t_NUM(t):
    r'\d+'
    return t

def t_VAR(t):
    r'[a-z]+'
    return t

def t_STR(t):
    r'\".+\"'
    return t

t_ignore = '\n\t '

def t_error(t):

    print(f'Caratér ilegal: {t.value[0]}')

    t.lexer.skip(1)

    return t

#Build the lexer

lexer = lex.lex()
