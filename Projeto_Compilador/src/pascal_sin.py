import ply.yacc as yacc
from pascal_lex import tokens, literals
from stack_generator import generate_code

# Definição da gramática
def p_program(p):
    '''program : PROGRAM id ';' declarations block '.' '''
    p[0] = ['program', p[2]] + [p[4]] + p[5] + [p[6]]

def p_block(p):
    '''block : BEGIN statements END terminator'''
    p[0] = [p[1]] + p[2] + [p[3]]


def p_declarations(p):
    '''declarations : VAR declaration_list ';' 
                    | CONST declaration_list ';' 
                    | VAR declaration_list  CONST declaration_list  
                    | CONST declaration_list  VAR declaration_list 
                    | '''
    if len(p) == 1:
        p[0] = ['var']
    elif len(p) == 4:
        p[0] = [p[1]] + p[2]
    elif len(p) == 5:
        p[0] = [p[1]] + p[2] + [p[3]] + p[4]

def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list ';' declaration'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_declaration(p):
    '''declaration : id_list ':' type'''
    p[0] = p[1] + [p[3]]

def p_id_list(p):
    '''id_list : id
               | id_list ',' id'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_type(p):
    '''type : INTEGER
            | REAL
            | STRING
            | CHAR
            | BOOLEAN
            | ARRAY '[' expression ']' OF type''' 
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = ['ARRAY', p[3], 'OF', p[6]]

def p_statements(p):
    '''statements : statement 
                  | statements statement '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : block
                 | assignment
                 | if_statement
                 | while_statement
                 | for_statement
                 | comments
                 | function_call'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : id ASSIGN expression'''
    p[0] = ["assign", p[1], p[3]]

def p_if_statement(p):
    '''if_statement : IF exprBool THEN statement ifCont'''
    if len(p[5]) == 0:
        p[0] = ['IF', p[2], ['THEN', p[4]]]
    else:
        p[0] = ['IF', p[2], ['THEN', p[4]], ['ELSE', p[5]]] 


def p_ifCont(p):
    '''ifCont : 
              | ELSE statement'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[2]]



def p_while_statement(p):
    '''while_statement : WHILE expression DO statement'''
    p[0] = ['WHILE'] + p[2] + ['DO'] + p[4]

def p_for_statement(p):
    '''for_statement : FOR id ASSIGN expression forCont'''
    p[0] = ['FOR', p[2], ':=', p[4]] + p[5]

def p_forCont(p):
    '''forCont : TO expression DO statement
                | DOWNTO expression DO statement'''
    p[0] = [p[1], p[2], 'DO', p[4]]

def p_exprBool(p):
    '''exprBool : expression
                | expression opRel expression
                | NOT expression'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = [p[2], p[1], p[3]]
    else:
        p[0] = ['NOT'] + p[2]

def p_opRel(p):
    '''opRel : '=' 
             | NOTEQUAL
             | '<'
             | '>'
             | MINOREQUALS
             | LARGEREQUALS '''
    p[0] = p[1]

def p_expression(p):
    '''expression : term
                  | expression opAdd term
                  | num TWODOTS num''' 
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '..':
        p[0] = [p[1], '..', p[3]]
    else:
        p[0] = [p[2], p[1], p[3]]

def p_opAdd(p):
    '''opAdd : '+'
             | '-'
             | OR'''
    p[0] = p[1]

def p_term(p):
    '''term : factor
             | term opMul factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[2], p[1], p[3]]

def p_opMul(p):
    '''opMul : '*'
             | '/'
             | '%'
             | AND
             | MOD
             | DIV'''
    p[0] = p[1]

def p_factor(p):
    '''factor : const terminator
              | var terminator
              | function_call
              | '(' exprBool ')' '''
    if len(p) == 3:
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_const(p):
    '''const : num
             | text
             | TRUE
             | FALSE'''
    p[0] = p[1]

def p_var(p):
    '''var : id
           | id '[' expression ']' '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1], p[3]]

def p_function_call(p):
    '''function_call : id '(' ')' terminator
                     | id '(' arg_list ')' terminator'''
    if len(p) >=5 :
        p[0] = [p[1] , p[3]] 
    else:
        p[0] = p[1]

def p_terminator(p):
    '''terminator : ';'
                  | '''

def p_arg_list(p):
    '''arg_list : expression
                | arg_list ',' expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_comments(p):
    '''comments : comment'''


# Erros de sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}' na linha {p.lineno}")
        print("Tipo de token:", p.type)
        parser.success = False

# Construção do parser
parser = yacc.yacc(debug=True)

import sys

parser.success = True
entrada = sys.stdin.read()  # Lê tudo de uma vez
resultado = parser.parse(entrada)

if parser.success:
    print(f"\nA representação intermédia do código é:\n\n{resultado}\n")
    with open(f'../outputs/{resultado[1]}.txt', 'w') as output:
        generate_code(resultado, output)
    print(f"Ficheiro de output gerado: {resultado[1]}.txt\n")