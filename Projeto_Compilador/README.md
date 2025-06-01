# Projeto de Compilador Pascal Standard
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
Para executar o nosso compilador basta correr no terminal, estando na pasta **/src**:
```
cat [path ficheiro teste] | python3 pascal_sin.py
```

## 3. O Compilador

### 3.1 Lexer (Tokens e Expressões Regulares)

O analisador léxico foi implementado com PLY.lex no ficheiro [pascal_lex.py](./src/pascal_lex.py). Define tokens, literais e as respetivas expressões regulares para reconhecimento. Para testar o funcionamento do analisador léxico, foi criado o ficheiro [tokenizer.py](./src/tokenizer.py). Para o ver funcionar basta escrever no terminal:
```
cat [path ficheiro teste] | python3 tokenizer.py 
```

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

A gramática do compilador Pascal foi implementada usando o módulo `yacc` da biblioteca PLY (Python Lex-Yacc). Esta gramática define as regras de construção sintática dos programas e segue uma estrutura típica das linguagens imperativas, inspirada no Pascal. Esta implementação encontra-se no ficheiro [pascal_sin.py](./src/pascal_sin.py)

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
Este árvore sintática encontra-se pronta para gerar o código máquina.

### 3.3 Gerador de código VM

#### Decisões e abordagens

Como a nossa abordagem foi traduzir os programas Pascal numa representação intermédia, criamos um novo ficheiro ([stack_generator.py](./src/stack_generator.py)) que percorre esta mesma, convertendo-a na linguagem VM pretendida.

Tal como demonstrado no exemplo anterior, a AST gerada foi planeada de modo a ter *tags* que auxiliam na geração do código VM.
Apresentam-se a seguir alguns exemplos da conversão da AST em código VM.

#### Declaração de variáveis
```python
...['var', ['n', 'i', 'fat', ['integer']]],
    'begin',...
```
```
PUSHI 0 -> coloca-se 0 no topo da stack para inicializar o inteiro "n"
STOREG 0 -> guarda-se o valor de "n" na posição 0 da stack
PUSHI 0 -> coloca-se 0 no topo da stack para inicializar o inteiro "i"
STOREG 1 -> guarda-se o valor de "n" na posição 0 da stack
PUSHI 0 -> coloca-se 0 no topo da stack para inicializar o inteiro "fat"
STOREG 2 -> guarda-se o valor de "fat" na posição 0 da stack
START -> começa o programa quando aparece a tag 'begin', iniciando o apontador na posição a seguir às variáveis
```

#### Ciclos FOR
```python
...[
      'FOR', 'i', ':=', 1, 'to', ['n'], 'DO',...
        ]
```
```
PUSHI 1 -> colocar o valor inicial do "i" na stack
STOREG 1 -> guardar o valor no endereço de "i"
L0: -> label de entrada no loop
PUSHG 1 -> carregar o valor de "i" para a stack
PUSHG 0 -> carregar o valor de "n" para a stack
INFEQ -> verificar se i <= n
JZ L1 -> se i > n saltar para a label L1
... (código a executar dentro do for)
PUSHG 1 -> carregar o valor de "i" para a stack
PUSHI 1 -> colocar o valor 1 na stack para incrementar o "i"
ADD -> somar 1 a "i"
STOREG 1 -> guardar o novo valor de "i" no seu endereço
JUMP L0 -> label de salto para o início do loop
L1: -> label de salto de fim do ciclo
... (código a executar depois do for)
```

#### Ciclos WHILE

```python
...['WHILE', 
        '<=', ['i'], 5, 
        'DO',...
    ]
```
```
L0: -> label de inicio do ciclo
PUSHG 0 -> carrega o valor de "i" para a stack
PUSHI 5 -> coloca o valor 5 na stack
INFEQ -> verifica a condição do ciclo while (se i <= 5) caso i > 5 a condição coloca 0 na stack
JZ L1 -> salta para L1 se a condição deu 0
... -> caso i <= 5 corre o código dentro do while
PUSHG 0 -> carrega o valor de "i" para a stack
PUSHI 1 -> coloca o valor 1 na stack para incrementar o "i"
ADD -> soma 1 a "i"
STOREG 0 -> atualiza o valor de "i"
JUMP L0 -> salta para o início do ciclo
L1: -> label de fim de ciclo
... -> continuação do programa
```

#### Expressões IF-THEN-ELSE

```python
['IF', ['>', ['numero'], 10], 
    
    ['THEN', ['writeln', ["'O número é maior que 10.'"]]],

['ELSE', [['writeln', ["'O número não é maior que 10.'"]]]]

],...
```

```
PUSHG 0 -> coloca o valor de "numero" na stack
PUSHI 10 -> coloca o valor 10 na stack
SUP -> verifica a condição do IF (se numero > 10) caso numero > 10 a condição coloca 0 na stack
JZ L0 -> salta para L0 se a condição deu 0, ou seja, salta para o ramo ELSE
PUSHS "O número é maior que 10." -> se a condição deu 1 executa o ramo THEN
WRITES -> imprime a string no stdout
WRITELN -> imprime "\n" no stdout
JUMP L1 -> salta para depois do ELSE
L0: -> label onde começa o ELSE
PUSHS "O número não é maior que 10." -> coloca a string na stack
WRITES -> imprime a string no stdout
WRITELN -> imprime "\n" no stdout
L1: label depois do ELSE
```

## 4. Testes

Para testar o funcionamento e correção do nosso compilador foram usados os testes presentes no enunciado.

1. O [teste 1](./tests/test1.pas) gerou o ficheiro [HelloWorld.txt](./outputs/HelloWorld.txt)
2. O [teste 2](./tests/test2.pas) gerou o ficheiro [Maior3.txt](./outputs/Maior3.txt)
3. O [teste 3](./tests/test3.pas) gerou o ficheiro [Fatorial.txt](./outputs/Fatorial.txt)
4. O [teste 4](./tests/test4.pas) gerou o ficheiro [NumeroPrimo.txt](./outputs/NumeroPrimo.txt)
5. O [teste 5](./tests/test5.pas) gerou o ficheiro [SomaArray.txt](./outputs/SomaArray.txt)
6. O [teste 6](./tests/test6.pas) gerou o ficheiro [BinarioParaInteiro.txt](./outputs/BinarioParaInteiro.txt)

## Conclusão

A implementação do compilador para a linguagem Pascal Standard permitiu aplicar os conceitos dados na unidade curricular de Processamento de Linguagens, percorrendo todas as fases de um compilador: análise léxica, análise sintática, análise semântica e geração de código.

A análise léxica foi realizada com expressões regulares usando `PLY.lex`, permitindo reconhecer tokens e literais. A análise sintática, com `PLY.yacc`, seguiu a gramática por nós definida, que permitiu reconhecer as estruturas da linguagem. A geração de código produziu instruções compatíveis com a máquina virtual EWWM, provando que o nosso compilador é funcional.

Este trabalho permitiu que, de uma maneira simples e numa escala menor, pudessemos aplicar de forma prática os conhecimentos teóricos adquiridos na UC. A ligação entre teoria (autómatos, gramáticas, parsers) e prática (tokens, AST, código VM) permitiu exclarecer o que acontece entre a linguagem de programação de alto nível e o codigo máquina.
