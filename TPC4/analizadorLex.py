import re

def anali_lex(entrada):
    
    regras = [
        ('RESERVADA', r'\b(?:select|where|limit)\b'),
        ('VARIAVEL',  r'\?[a-zA-Z_][a-zA-Z0-9_]*'),
        ('NOME_IRI',  r'(dbo|foaf):[a-zA-Z_][a-zA-Z0-9_]*'),
        ('CADEIA',    r'"[^"\n]*"(?:@[a-zA-Z\-]+)?'),
        ('NUMERO',    r'\d+'),
        ('DELIMITADOR', r'[{}.]'),
        ('ESPACO',    r'\s+'),
        ('ERRO',      r'.'),
    ]

    regex_global = '|'.join(f'(?P<{tipo}>{padrao})' for tipo, padrao in regras)
    analise = [] 

    for m in re.finditer(regex_global, entrada, re.IGNORECASE):
        tipo = m.lastgroup
        valor = m.group(tipo)

        if tipo == 'ESPACO':
            continue
        elif tipo == 'ERRO':
            print(f"Aviso: símbolo não reconhecido -> {valor}")
        else:
            analise.append((valor, tipo))

    return analise


# --- Exemplo de utilização ---
if __name__ == "__main__":
    consulta = """
    SELECT ?nome ?desc WHERE {
        ?s a dbo:MusicalArtist.
        ?s foaf:name "Chuck Berry"@en .
        ?w dbo:artist ?s.
        ?w foaf:name ?nome.
        ?w dbo:abstract ?desc
    } LIMIT 1000
    """

    tokens = anali_lex(consulta)

    print("Tokens identificados:")
    for valor, tipo in tokens:
        print(f"{tipo:<12} → {valor}")
