import ply.lex as lex

# List of literal tokens
literals = ['+', '-', '*', '/', '%', '(', ')', ';', ':', '=', ',', '.', 
            '<', '>', '[', ']', '{', '}']

# Palavras reservadas e seus tokens
reserved = {
    'program': 'PROGRAM',
    'begin': 'BEGIN',
    'end': 'END',
    'var': 'VAR',
    'integer': 'INTEGER',
    'real': 'REAL',
    'string': 'STRING',
    'char': 'CHAR',
    'boolean': 'BOOLEAN',
    'array': 'ARRAY',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'do': 'DO',
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR',
    'true': 'TRUE',
    'false': 'FALSE',
    'of': 'OF',
    'to': 'TO',
    'downto': 'DOWNTO',
    'div': 'DIV',
    'mod': 'MOD',
    'const': 'CONST',
}

# Lista final de tokens
tokens = [
    'id', 'num', 'text', 'comment',
    'MINOREQUALS', 'LARGEREQUALS', 'NOTEQUAL', 'TWODOTS', 'ASSIGN'
] + list(reserved.values())

# Ignorar espaços e tabs
t_ignore = ' \t'

# Tokens simples com regex
def t_ASSIGN(t): r':='; return t
def t_MINOREQUALS(t): r'<='; return t
def t_LARGEREQUALS(t): r'>='; return t
def t_NOTEQUAL(t): r'<>'; return t
def t_TWODOTS(t): r'\.\.'; return t

# Tokens variáveis
def t_id(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value.lower(), 'id')  # verifica se é palavra reservada
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

# Construir o lexer
lexer = lex.lex()
