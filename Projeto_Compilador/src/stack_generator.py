symbol_table = {}
var_offset = 0
label_counter = [0]
started = False 

def generate_code(resultado, output):
    global started
    for elem in resultado:
        if elem == 'program':
            print(f"A gerar código para o programa: {resultado[1]}\n")
        elif isinstance(elem, list) and len(elem) > 0:
            keyword = elem[0].lower()
            if keyword == 'var':
                handle_declarations(elem, output)
            elif keyword == 'assign':
                handle_assignment(elem, output)
            elif keyword == 'if':
                handle_if(elem, output)
            elif keyword == 'readln':
                handle_read(elem, output)
            elif keyword == 'write':
                handle_writeln(elem, output)
            elif keyword == 'writeln':
                handle_writeln(elem, output)
            elif keyword == '.':
                output.write("STOP\n")
            elif keyword == 'while':
                 handle_while(elem, output)
            elif keyword == 'for':
                 handle_for(elem, output)
            else:
                generate_code(elem, output)
        elif elem == 'begin':
            if not started:
                output.write("START\n")
                started = True
        elif elem == '.':
            output.write("STOP\n")
        
def handle_read(elem, output):
    args = elem[1]
    if not isinstance(args, list):
        args = [args]
    if len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], list):
        args = [args]
    # Se os argumentos forem listas aninhadas com um único elemento, simplifique
    new_args = []
    for arg in args:
        if isinstance(arg, list) and len(arg) == 1:
            new_args.append(arg[0])
        else:
            new_args.append(arg)
    args = new_args
    for var in args:
        if isinstance(var, list):
            if len(var) == 2 and isinstance(var[0], str) and isinstance(var[1], list):
                varname = var[0]
                index_expr = var[1]
                if varname in symbol_table:
                    var_info = symbol_table[varname]
                    if var_info['type'] == 'array':
                        output.write(f"PUSHG {var_info['offset']}\n")
                        generate_expression(index_expr, output)
                        output.write("PUSHI 1\nSUB\n")
                        output.write("READ\n")
                        output.write("ATOI\n")
                        output.write("STOREN\n")
        elif isinstance(var, str):
            if var in symbol_table:
                var_info = symbol_table[var]
                if var_info['type'] == 'int':
                    output.write("READ\n")
                    output.write("ATOI\n")
                    output.write(f"STOREG {var_info['offset']}\n")
                elif var_info['type'] == 'string':
                    output.write(f"READ\n")
                    output.write(f"STOREG {var_info['offset']}\n")
                else:
                    print(f"Erro: '{var}' não é variável simples.")
            else:
                print(f"Erro: variável '{var}' não declarada.")
        else:
            print(f"Erro: argumento para readln malformado: {var}")

def handle_declarations(elem, output):
    global var_offset
    if len(elem) == 1:
        return
    args = elem[1:]  # ignora o 'var'
    for types in args:
        vars_type = types[-1]
        # Caso tipo seja ['integer'], ['boolean'], etc.
        if isinstance(vars_type, list) and len(vars_type) == 1 and isinstance(vars_type[0], str):
            vars_type = vars_type[0]
        num_vars = len(types) - 1
        # Verifica se é array
        if isinstance(vars_type, list) and vars_type[0] == 'ARRAY':
            array_bounds = vars_type[1]  # [1, '..', 5]
            lower_bound = array_bounds[0]
            upper_bound = array_bounds[2]
            tamanho = upper_bound - lower_bound + 1
            for var in types[:-1]:
                symbol_table[var] = {
                    'offset': var_offset,
                    'type': 'array',
                    'size': tamanho,
                    'lower_bound': lower_bound
                }
                output.write(f"PUSHI {tamanho}\n")
                output.write("ALLOCN\n")
                output.write(f"STOREG {var_offset}\n")
                var_offset += 1
        # Verifica tipos básicos
        elif isinstance(vars_type, str):
            for var in types[:-1]:
                t = vars_type.lower()
                if t == 'string':
                    symbol_table[var] = {'offset': var_offset, 'type': 'string'}
                elif t == 'integer':
                    symbol_table[var] = {'offset': var_offset, 'type': 'int'}
                    output.write(f"PUSHI 0\n")
                    output.write(f"STOREG {var_offset}\n")
                elif t == 'boolean':
                    symbol_table[var] = {'offset': var_offset, 'type': 'bool'}
                else:
                    print(f"Tipo não suportado na declaração: {vars_type}")
                var_offset += 1
        else:
            print(f"Tipo de variável inesperado: {vars_type}")


def handle_assignment(elem, output):
    varname = elem[1]
    expr = elem[2]
    if isinstance(varname, str):
        # Trata variável simples
        if varname in symbol_table:
            var_info = symbol_table[varname]
            generate_expression(expr, output)
            output.write(f"STOREG {var_info['offset']}\n")
        else:
            print(f"Erro: variável '{varname}' não declarada.")
    else:
        print(f"Erro: forma de variável não reconhecida: {varname}")

def unwrap_varname(var):
    while isinstance(var, list) and len(var) == 1:
        var = var[0]
    return var

def generate_expression(expr, output):
    if isinstance(expr, list):
        if expr[0].lower() == 'length':
            # expr exemplo: ['length', [varname]]
            varname = unwrap_varname(expr[1])
            if varname in symbol_table:
                var_info = symbol_table[varname]
                if var_info['type'] == 'string':
                    output.write(f"PUSHG {var_info['offset']}\n")
                    output.write("STRLEN\n")
                else:
                    print(f"Erro: variável '{varname}' não é array para length.")
            else:
                print(f"Erro: variável '{varname}' não declarada para length.")
            return
        # Caso 1: operador binário
        if len(expr) == 3:
            op, left, right = expr
            # Gera as expressões
            generate_expression(left, output)
            generate_expression(right, output)
            # Gera operação
            if op == '+':
                output.write("ADD\n")
            elif op == '-':
                output.write("SUB\n")
            elif op == '*':
                output.write("MUL\n")
            elif op == '/':
                output.write("DIV\n")
            elif op == 'mod':
                output.write("MOD\n")
            elif op == 'div':
                output.write("DIV\n")
            elif op == '=':
                output.write("EQUAL\n")
            elif op in ['<>', '!=']:
                output.write("EQUAL\n")
                output.write("NOT\n")
            elif op == '<':
                output.write("INF\n")
            elif op == '<=':
                output.write("INFEQ\n")
            elif op == '>':
                output.write("SUP\n")
            elif op == '>=':
                output.write("SUPEQ\n")
            elif op.lower() == 'and':
                output.write("AND\n")
            elif op.lower() == 'or':
                output.write("OR\n")
            else:
                print(f"Erro: operador '{op}' não suportado.")
        # Caso 2: operador unário NOT
        elif len(expr) == 2 and expr[0] == 'NOT':
            generate_expression(expr[1], output)
            output.write("NOT\n")
        # Caso 3: acesso a elemento de array: ['nome_array', indice]
        elif len(expr) == 2:
            varname, index_expr = expr
            if varname in symbol_table:
                var_info = symbol_table[varname]

                if var_info['type'] == 'array':
                    output.write(f"PUSHG {var_info['offset']}\n") 
                    generate_expression(index_expr,output)
                    output.write("PUSHI 1\n")
                    output.write("SUB\nLOADN\n")  # ajusta índice para base 0
                elif var_info['type'] == 'string':
                     # Gerar código para CHARAT
                    generate_expression(index_expr, output)  # empilha índice
                    output.write("PUSHI 1\nSUB\n")  # ajusta índice para base 0
                    output.write(f"PUSHG {var_info['offset']}\n")  # empilha string (endereço)
                    output.write("SWAP\n")  # corrige a ordem
                    output.write("CHARAT\n")  # pega o caractere ASCII na posição
                else:
                    print(f"Erro: '{varname}' não é array.")
            else:
                print(f"Erro: variável '{varname}' não declarada.")
        # Caso 4: expressão simples dentro de lista (ex: ['x'])
        elif len(expr) == 1:
            generate_expression(expr[0], output)
        else:
            print(f"Erro: expressão malformada: {expr}")
    elif isinstance(expr, str):
        lowered = expr.lower()
        if lowered == 'true':
            output.write("PUSHI 1\n")
        elif lowered == 'false':
            output.write("PUSHI 0\n")
        elif expr.isdigit():
            output.write(f"PUSHI {expr}\n")
        elif expr.startswith("'") and expr.endswith("'") and len(expr) == 3:
            output.write(f"PUSHI {ord(expr[1])}\n")
        elif expr in symbol_table:
            var_info = symbol_table[expr]
            if var_info['type'] in ['int', 'bool']:
                output.write(f"PUSHG {var_info['offset']}\n")
            else:
                print(f"Erro: '{expr}' não é variável simples.")
        else:
            print(f"Erro: identificador '{expr}' não declarado.")
    elif isinstance(expr, int):
        output.write(f"PUSHI {expr}\n")
    else:
        print(f"Erro: tipo de expressão não suportado: {expr}")

def handle_writeln(elem, output):
    args = elem[1]
    for arg in args:
        if isinstance(arg, str) and arg.startswith("'") and arg.endswith("'"):
            expr_content = arg[1:-1]  # remove as aspas simples
            output.write(f'PUSHS "{expr_content}"\nWRITES\n')
        else:
            varname = unwrap_varname(arg)
            if varname in symbol_table:
                var_info = symbol_table[varname]
                if var_info['type'] == 'int':
                    output.write(f"PUSHG {var_info['offset']}\nWRITEI\n")
                elif var_info['type'] == 'string':
                    output.write(f"PUSHG {var_info['offset']}\nWRITES\n")
                else:
                    output.write(f"# Tipo desconhecido para {varname}\n")
            else:
                output.write(f"# Não sei como escrever {arg}\n")
    output.write("WRITELN\n")

def new_label():
    label = f"L{label_counter[0]}"
    label_counter[0] += 1
    return label

def handle_if(elem, output):
    cond = elem[1]
    then_block = elem[2][1]  # ['then', <bloco>]
    else_block = elem[3][1] if len(elem) > 3 else None
    if not isinstance(then_block, list) or (then_block and not isinstance(then_block[0], list)):
        then_block = [then_block]
    if else_block and (not isinstance(else_block, list) or (else_block and not isinstance(else_block[0], list))):
        else_block = [else_block]
    label_else = new_label()
    label_end = new_label()
    generate_expression(cond, output)
    output.write(f"JZ {label_else}\n")
    for stmt in then_block:
        generate_code([stmt], output)
    output.write(f"JUMP {label_end}\n")
    output.write(f"{label_else}:\n")
    if else_block:
        for stmt in else_block:
            generate_code([stmt], output)
    output.write(f"{label_end}:\n")


def handle_while(elem, output):
    try:
        do_index = elem.index('DO')
    except ValueError:
        raise ValueError("Estrutura 'WHILE ... DO ...' malformada")
    condition_part = elem[1:do_index]
    body_part = elem[do_index + 1:]
    # Extrai a expressão da condição
    cond_expr = condition_part[0] if len(condition_part) == 1 else condition_part
    # Normaliza corpo para lista de instruções
    if isinstance(body_part, list) and len(body_part) == 1 and isinstance(body_part[0], list):
        body = body_part[0]
    else:
        body = body_part
    if not isinstance(body, list) or (body and not isinstance(body[0], list)):
        body = [body]
    label_start = new_label()
    label_end = new_label()
    output.write(f"{label_start}:\n")
    generate_expression(cond_expr, output)
    output.write(f"JZ {label_end}\n")
    for stmt in body:
        generate_code([stmt], output)
    output.write(f"JUMP {label_start}\n")
    output.write(f"{label_end}:\n")


def handle_for(elem, output):
    # Estrutura esperada: ['FOR', var, ':=', start, 'to'/'downto', end, 'DO', body]
    if len(elem) < 8 or elem[2] != ':=' or elem[6].lower() != 'do':
        raise ValueError("Erro: estrutura do FOR inválida.")
    varname = elem[1]
    start_val = elem[3]
    direction = elem[4].lower()
    end_val = elem[5]
    body = elem[7]
    # Verifica se a variável de controle foi declarada
    if varname not in symbol_table:
        raise ValueError(f"Erro: variável '{varname}' não declarada no FOR.")
    # Inicializa a variável de controle com o valor inicial
    generate_expression(start_val, output)
    output.write(f"STOREG {symbol_table[varname]['offset']}\n")
    # Criação de labels para controle de fluxo
    label_start = new_label()
    label_end = new_label()
    output.write(f"{label_start}:\n")
    # Gera condição do laço
    output.write(f"PUSHG {symbol_table[varname]['offset']}\n")  # variável
    generate_expression(end_val, output)  # valor final
    if direction == 'to':
        output.write("INFEQ\n")  # var <= end_val
    elif direction == 'downto':
        output.write("SUPEQ\n")  # var >= end_val
    else:
        raise ValueError(f"Erro: direção do FOR desconhecida: {direction}")
    output.write(f"JZ {label_end}\n")  # se condição falsa, sai do laço
    # Garante que o corpo seja sempre uma lista de comandos
    if not isinstance(body, list) or (body and not isinstance(body[0], list)):
        body = [body]
    for stmt in body:
        generate_code([stmt], output)
    # Incrementa ou decrementa a variável de controle
    output.write(f"PUSHG {symbol_table[varname]['offset']}\n")
    if direction == 'to':
        output.write("PUSHI 1\nADD\n")
    else:  # downto
        output.write("PUSHI 1\nSUB\n")
    output.write(f"STOREG {symbol_table[varname]['offset']}\n")
    # Volta para o início do laço
    output.write(f"JUMP {label_start}\n")
    output.write(f"{label_end}:\n")
