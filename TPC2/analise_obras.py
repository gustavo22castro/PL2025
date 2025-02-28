import sys

NOME = 0
DESC = 1
ANO = 2
PERIODO = 3
COMPOSITOR = 4
DURACAO = 5
ID = 6

def parse_csv(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            texto = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{path}' não encontrado.")
        sys.exit(1)

    rows = []
    current_row = []
    field = []
    dentro_aspas = False

    for char in texto:
        if char == '"':
            dentro_aspas = not dentro_aspas
        elif char == '\n' and not dentro_aspas:
            # Fim de linha
            current_row.append(''.join(field).strip())
            rows.append(current_row)
            current_row = []
            field = []
        elif char == ';' and not dentro_aspas:
            # Adiciona o campo à linha atual
            current_row.append(''.join(field).strip())
            field = []
        else:
            field.append(char)

    # Adiciona o último campo e linha, se necessário
    if field:
        current_row.append(''.join(field).strip())
    if current_row:
        rows.append(current_row)
    
    # Remover o cabeçalho
    rows = rows[1:]

    obras = []
    for campos in rows:
        # Garante que a linha tenha exatamente 7 campos
        if len(campos) != 7:
            print(f"Linha ignorada (número errado de campos): {';'.join(campos)}")
            continue

        try:
            nome = campos[NOME]
            desc = campos[DESC]
            ano = int(campos[ANO]) if campos[ANO].isdigit() else None
            periodo = campos[PERIODO]
            compositor = campos[COMPOSITOR]
            duracao = int(campos[DURACAO]) if campos[DURACAO].isdigit() else None
            id = int(campos[ID]) if campos[ID].isdigit() else None

            obras.append((nome, desc, ano, periodo, compositor, duracao, id))
        except ValueError as e:
            print(f"Erro ao converter valores na linha: {';'.join(campos)} - {e}")
            continue

    return obras

def main():
    if len(sys.argv) < 2:
        print("Uso: python script.py <caminho_para_arquivo.csv>")
        sys.exit(1)
    
    obras = parse_csv(sys.argv[1])

    compositores = []
    obras_por_periodo = {}

    for obra in obras:
        compositor = obra[COMPOSITOR]
        if compositor not in compositores:
            compositores.append(compositor)
        
        periodo = obra[PERIODO]
        if periodo not in obras_por_periodo:
            obras_por_periodo[periodo] = []
        obras_por_periodo[periodo].append(obra)

    # 1 - Ordenar compositores alfabeticamente
    compositores.sort()
    print('Compositores:', compositores)

    # 2 - Exibir o número de obras de cada período
    for periodo, list_obras in obras_por_periodo.items():
        print(f"Número de obras do período {periodo}: {len(list_obras)}")

    # 3 - Exibir as obras ordenadas alfabeticamente por período
    for periodo, list_obras in sorted(obras_por_periodo.items()):
        print(f"Obras do período {periodo}:")
        for obra in sorted(list_obras, key=lambda o: o[NOME]):
            print(obra[NOME])

if __name__ == '__main__':
    main()
