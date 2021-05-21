import ply.lex as lex

tokens = ['INT', 'VAR', 'NUM', 'BEGIN_INSTRS', 'END_INSTRS']
literals = [',', '=', ';', '+', '-', '*', '/', '(', ')', '{', '}']

def t_BEGIN_INSTRS(t):
    r'BEGIN'
    return t

def t_END_INSTRS(t):
    r'END\.'
    return t

def t_INT(t):
    r'INT'
    return t

def t_NUM(t):
    r'\d+'
    return t

def t_VAR(t):
    r'[a-z]+'
    return t

t_ignore = '\n\t '

def t_error(t):

    print(f'Caratér ilegal: {t.value[0]}')

    t.lexer.skip(1)

    return t

#Build the lexer

lexer = lex.lex()
