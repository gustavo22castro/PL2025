import sys
from pascal_lex import lexer

data = sys.stdin.read()
lexer.input(data)

print("Tokens reconhecidos:")
for tok in lexer:
    print(tok)