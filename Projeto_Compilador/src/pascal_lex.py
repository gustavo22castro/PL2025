import ply.lex as lex

# List of literal tokens
literals = ['+', '-', '*', '/', '%', '(', ')', ';', ':', '=', ',', '.', 
            '<', '>', '[', ']', '{', '}']

# Tokens incluindo operadores compostos
tokens = ['id', 'num', 'text', 'comment', 'MINOREQUALS', 'LARGEREQUALS', 'NOTEQUAL', 'TWODOTS', 'ASSIGN',
          'PROGRAM', 'BEGIN', 'END', 'VAR', 'INTEGER', 'REAL', 'STRING', 'CHAR', 'BOOLEAN',
          'ARRAY', 'IF', 'THEN', 'ELSE', 'WHILE', 'FOR', 'DO', 'NOT', 'AND',
          'OR', 'TRUE', 'FALSE', 'OF', 'TO', 'DOWNTO', 'DIV', 'MOD', 'CONST'] 

# Ignorar espaços e tabs
t_ignore = ' \t'

def t_PROGRAM(t):
    r'(?i)(program)'
    return t

def t_BEGIN(t):
    r'(?i)(begin)'
    return t

def t_END(t):
    r'(?i)(end)'
    return t

def t_VAR(t):
    r'(?i)(var)'
    return t

def t_INTEGER(t):
    r'(?i)(integer)'
    return t

def t_REAL(t):
    r'(?i)(real)'
    return t

def t_STRING(t):
    r'(?i)(string)'
    return t

def t_CHAR(t):
    r'(?i)(char)'
    return t

def t_BOOLEAN(t):
    r'(?i)(boolean)'
    return t

def t_ARRAY(t):
    r'(?i)(array)'
    return t

def t_IF(t):
    r'(?i)(if)'
    return t

def t_THEN(t):
    r'(?i)(then)'
    return t

def t_ELSE(t):
    r'(?i)(else)'
    return t

def t_WHILE(t):
    r'(?i)(while)'
    return t

def t_FOR(t):
    r'(?i)(for)'
    return t

def t_DOWNTO(t):
    r'(?i)(downto)'
    return t

def t_DO(t):
    r'(?i)(do)'
    return t

def t_NOT(t):
    r'(?i)(not)'
    return t

def t_AND(t):
    r'(?i)(and)'
    return t

def t_OR(t):
    r'(?i)(or)'
    return t

def t_TRUE(t):
    r'(?i)(true)'
    return t

def t_FALSE(t):
    r'(?i)(false)'
    return t

def t_OF(t):
    r'(?i)(of)'
    return t

def t_TO(t):
    r'(?i)(to)'
    return t

def t_DIV(t):
    r'(?i)(div)'
    return t

def t_MOD(t):
    r'(?i)(mod)'
    return t

def t_ASSIGN(t):
    r':='
    return t

def t_MINOREQUALS(t):
    r'<='
    return t

def t_LARGEREQUALS(t):
    r'>='
    return t

def t_NOTEQUAL(t):
    r'<>'
    return t

def t_TWODOTS(t):
    r'\.\.'
    return t

def t_CONST(t):
    r'(?i)(const)'
    return t

def t_id(t):
    r'[a-zA-Z_]\w*'
    return t

def t_num(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_text(t):
    r'\'([^\\\n\']|\\.)*\''
    return t

def t_comment(t):
    r'\{[^}]*\}'
    pass  # Ignora comentários

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
