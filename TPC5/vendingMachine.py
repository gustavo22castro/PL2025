import sys
import json
import re
from datetime import date

stock = {}
saldo = 0.0

moedas_disponiveis = [2.00, 1.00, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01]

def carregar_dados(caminho):
    try:
        with open(caminho, 'r') as f:
            dados = json.load(f)
        for item in dados["stock"]:
            stock[item["cod"]] = item
        return True
    except Exception as e:
        print(f"Erro ao carregar stock: {e}")
        return False

def guardar_dados(caminho):
    with open(caminho, 'w') as f:
        json.dump({"stock": list(stock.values())}, f, indent=2)

def listar():
    print("\nCódigo | Produto               | Quantidade | Preço")
    print("-------+------------------------+------------+-------")
    for item in stock.values():
        print(f"{item['cod']: <6} | {item['nome']: <22} | {item['quant']: <10} | {item['preco']:.2f}€")

def inserir_moedas(texto):
    global saldo
    moedas = re.findall(r'(\d+)(e|c)', texto)
    for val, tipo in moedas:
        valor = int(val) / 100 if tipo == 'c' else int(val)
        saldo += valor
    print(f"Saldo atual: {saldo:.2f}€")

def selecionar(cod):
    global saldo
    produto = stock.get(cod)
    if not produto:
        print("Produto inexistente.")
        return
    if produto['quant'] <= 0:
        print("Produto esgotado.")
        return
    if saldo < produto['preco']:
        print(f"Saldo insuficiente. Saldo = {saldo:.2f}€, Preço = {produto['preco']:.2f}€")
        return
    produto['quant'] -= 1
    saldo -= produto['preco']
    print(f"Produto '{produto['nome']}' dispensado. Saldo restante: {saldo:.2f}€")

def calcular_troco(valor):
    troco = {}
    restante = round(valor, 2)
    for moeda in moedas_disponiveis:
        count = int(restante // moeda)
        if count > 0:
            troco[moeda] = count
            restante = round(restante - count * moeda, 2)
    return troco

def formatar_troco(troco_dict):
    partes = []
    for valor, qtd in troco_dict.items():
        if valor >= 1.0:
            partes.append(f"{qtd}x {int(valor)}e")
        else:
            partes.append(f"{qtd}x {int(valor * 100)}c")
    return ', '.join(partes)


def sair():
    global saldo
    if saldo > 0:
        troco = calcular_troco(saldo)
        troco_str = formatar_troco(troco)
        print(f"maq: Pode retirar o troco: {troco_str}")
    print("maq: Até à próxima!")

def processar_linha(linha):
    linha = linha.strip()
    if re.match(r'(?i)^LISTAR$', linha):
        listar()
    elif re.match(r'(?i)^SAIR$', linha):
        sair()
        return False
    elif re.match(r'(?i)^MOEDA\s', linha):
        inserir_moedas(linha)
    elif re.match(r'(?i)^SELECIONAR\s+[a-zA-Z0-9]+$', linha):
        codigo = linha.split()[1].strip()
        selecionar(codigo)
    else:
        print("Comando não reconhecido.")
    return True

def main():
    if len(sys.argv) != 2:
        print("Uso: python vending.py <ficheiro_stock.json>")
        return

    caminho = sys.argv[1]
    if not carregar_dados(caminho):
        return

    print(f"maq: {date.today()}, stock carregado. Pronto para atender pedidos.\n")

    try:
        while True:
            linha = input(">> ")
            if not processar_linha(linha):
                break
    except KeyboardInterrupt:
        print("\nmaq: Encerrado pelo utilizador.")
    finally:
        guardar_dados(caminho)

if __name__ == "__main__":
    main()
