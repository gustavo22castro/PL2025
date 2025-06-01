# Projeto de Compilador vSL
**Processamento de Linguagens - LEI**

## 1. Introdução

Este projeto consiste na construção de um compilador para **Pascal Standard**. O compilador foi desenvolvido em Python utilizando a biblioteca `PLY` (Python Lex-Yacc) e cria código compatível com a máquina virtual fornecida **EWVM**.

---

## 2. Estrutura do Projeto

```bash
.
├── src/
│   ├── pascal_lex.py      # Analisador léxico
│   ├── pascal_sin.py      # Analisador sintático
│   ├── stack_generator.py # Gerador do código VM
│   └── tokenizer.py       # Ferramenta de debug dos tokens
├── tests/                 # Ficheiros de teste em Pascal (.pas)
├── outputs/               # Código VM gerado (.txt)
└── README.md              # Relatório
```

## 3. O Compilador

### 3.1 Lexer (Tokens e Expressões Regulares)

O analisador léxico foi implementado com PLY.lex no ficheiro pascal_lex.py. Define tokens, literais e as respetivas expressões regulares para reconhecimento.

Literais:

```python
literals = ['+', '-', '*', '/', '%', '(', ')', ';', ':', '=', ',', '.', '<', '>', '[', ']', '{', '}']
```

Tokens definidos:
```python
tokens = [
    'id', 'num', 'text', 'comment',
    'MINOREQUALS', 'LARGEREQUALS', 'NOTEQUAL', 'TWODOTS', 'ASSIGN',
    'PROGRAM', 'BEGIN', 'END', 'VAR', 'INTEGER', 'REAL', 'STRING',
    'CHAR', 'BOOLEAN', 'ARRAY', 'IF', 'THEN', 'ELSE', 'WHILE', 'FOR', 'DO',
    'NOT', 'AND', 'OR', 'TRUE', 'FALSE', 'OF', 'TO', 'DOWNTO', 'DIV', 'MOD', 'CONST'
]
```
As palavras-chave são definidas individualmente. Exemplo:
```python
def t_PROGRAM(t): r'(?i)(program)'; return t
def t_BEGIN(t):   r'(?i)(begin)'; return t
# ... as restantes são iguais para cada palavra-chave
```
#### Expressões regulares dos terminais variáveis

**Identificadores:** começam por letra ou underscore, seguidos de letras, números ou ```_```.
```python
def t_id(t):
    r'[a-zA-Z_]\w*'
    return t
```
**Números:** inteiros ou reais com ponto decimal.
```python
def t_num(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t
```
**Textos(strings):** delimitados por aspas simples ```'texto'```.
```python
def t_text(t):
    r'\'([^\\\n\']|\\.)*\''
    return t
```
**Comentários:** ```{...}```, ignorados no parsing.
```python
def t_comment(t):
    r'\{[^}]*\}'
    pass
```

#### Ignorar espaços
Estes caracteres não são tokens, mas aparecem no código-fonte. O lexer deve ignorá-los:

```python
t_ignore = ' \t'
```
#### Reconhecer novas linhas
O PLY precisa saber quando uma nova linha é encontrada para atualizar o número da linha:
```python
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
```

#### Tratamento de erros léxicos
Quando o lexer encontra um carácter ilegal, ele chama ``t_error``:
```python
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)
```
Esta função permite que a análise continue mesmo quando há erros e que estes possam ser vistos mais tarde.

### 3.2 Gramática (Parser)

A gramática do compilador vSL foi implementada usando o módulo `yacc` da biblioteca PLY (Python Lex-Yacc). Esta gramática define as regras de construção sintática dos programas e segue uma estrutura típica das linguagens imperativas, inspirada no Pascal.

Cada regra da gramática é escrita como uma função `p_<nome>` em Python, e o corpo da produção está numa string com notação BNF. O resultado de cada regra é armazenado em `p[0]`, como um nó de uma árvore sintática abstrata (AST).

---

#### Estrutura geral da linguagem

Gramática em bnf:

```bnf
program       ::= 'PROGRAM' id ';' declarations block '.'

declarations  ::= 'VAR' declaration_list ';'
                | 'CONST' declaration_list ';'
                | 'VAR' declaration_list 'CONST' declaration_list
                | 'CONST' declaration_list 'VAR' declaration_list
                | ε

declaration_list ::= declaration
                   | declaration_list ';' declaration

declaration   ::= id_list ':' type

id_list       ::= id
                | id_list ',' id

type          ::= 'INTEGER'
                | 'REAL'
                | 'STRING'
                | 'CHAR'
                | 'BOOLEAN'
                | 'ARRAY' '[' expression ']' 'OF' type

block         ::= 'BEGIN' statements 'END' terminator

statements    ::= statement
                | statements statement

statement     ::= block
                | assignment
                | if_statement
                | while_statement
                | for_statement
                | comments
                | function_call

assignment    ::= id ':=' expression

if_statement  ::= 'IF' exprBool 'THEN' statement ifCont

ifCont        ::= ε
                | 'ELSE' statement

while_statement ::= 'WHILE' expression 'DO' statement

for_statement ::= 'FOR' id ':=' expression forCont

forCont       ::= 'TO' expression 'DO' statement
                | 'DOWNTO' expression 'DO' statement

exprBool      ::= expression
                | expression opRel expression
                | 'NOT' expression

opRel         ::= '=' | '<>' | '<' | '>' | '<=' | '>='

expression    ::= term
                | expression opAdd term
                | num '..' num

opAdd         ::= '+' | '-' | 'OR'

term          ::= factor
                | term opMul factor

opMul         ::= '*' | '/' | '%' | 'AND' | 'MOD' | 'DIV'

factor        ::= const terminator
                | var terminator
                | function_call
                | '(' exprBool ')'

const         ::= num | text | 'TRUE' | 'FALSE'

var           ::= id
                | id '[' expression ']'

function_call ::= id '(' ')' terminator
                | id '(' arg_list ')' terminator

arg_list      ::= expression
                | arg_list ',' expression

terminator    ::= ';'
                | ε

comments      ::= comment
```
Exemplos de definição da gramática em python:
```python
def p_program(p):
    'program : PROGRAM id ";" declarations block "."'
    p[0] = ('programa', p[2], p[4], p[5])

def p_declarations(p):
    'declarations : VAR declaration_list'
    p[0] = p[2]

def p_statement_assignment(p):
    'statement : id ASSIGN expression'
    p[0] = ('assign', p[1], p[3])

def p_expression_add(p):
    'expression : expression PLUS term'
    p[0] = ('add', p[1], p[3])
```
Estas funções permitem construir a AST, que posteriormente será usada para produzir instruções da máquina virtual.

#### Exemplo Ilustrativo

Iremos demonstrar como a gramática funciona com um exemplo prático:

```Pascal
program Fatorial;
var
    n, i, fat: integer;
begin
    writeln('Introduza um número inteiro positivo:');
    readln(n);
    fat := 1;
    for i := 1 to n do
        fat := fat * i;
    writeln('Fatorial de ', n, ': ', fat);
end.
```
Após passar pelo pascal_sin.py temos a seguinte AST:

```python
[
  'program', 'Fatorial',
  ['var', ['n', 'i', 'fat', ['integer']]],
  'begin',
    ['writeln', ["'Introduza um número inteiro positivo:'"]],
    ['readln', [['n']]],
    ['assign', 'fat', 1],
    [
      'FOR', 'i', ':=', 1, 'to', ['n'], 'DO',
      ['assign', 'fat', ['*', ['fat'], ['i']]]
    ],
    ['writeln', [
        "'Fatorial de '",
        ['n'],
        "': '",
        ['fat']
    ]],
  'end',
  '.'
]
```
Este árvore sintática encontra-se pronta para gerar o código maquina.

## Conclusão

A implementação do compilador para a linguagem Pascal Standard permitiu aplicar os conceitos dados na unidade curricular de Processamento de Linguagens, percorrendo todas as fases de um compilador: análise léxica, análise sintática, análise semântica e geração de código.

A análise léxica foi realizada com expressões regulares usando `PLY.lex`, permitindo reconhecer tokens e literais. A análise sintática, com `PLY.yacc`, seguiu a gramática por nós definida, que permitiu reconhecer as estruturas da linguagem. A geração de código produziu instruções compatíveis com a máquina virtual EWWM, provando que o nosso compilador é funcional.

Este trabalho permitiu que, de uma maneira simples e numa escala menor, pudessemos aplicar de forma prática os conhecimentos teóricos adquiridos na UC. A ligação entre teoria (autómatos, gramáticas, parsers) e prática (tokens, AST, código VM) permitiu exclarecer o que acontece entre a linguagem de programação de alto nível e o codigo máquina.
