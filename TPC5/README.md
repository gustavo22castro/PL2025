# TPC5 – Máquina de Vending

## Autor
Gustavo Castro - A100482

## Objetivo

Este trabalho tem como objetivo desenvolver um programa que simula uma máquina de vending. Esta disponibiliza produtos com stock provenientes de um ficheiro json e permite inserir moedas, selecionar produtos e obter troco detalhado via terminal.

---

## Funcionalidades

- Carregamento do stock a partir de um ficheiro JSON.
- Comandos interativos:
  - `LISTAR` — Mostra os produtos disponíveis.
  - `MOEDA <valores>` — Adiciona moedas ao saldo (ex: `MOEDA 1e, 20c, 5c`).
  - `SELECIONAR <CÓDIGO>` — Compra um produto (se houver saldo e stock).
  - `SAIR` — Termina a sessão e devolve o troco detalhado em moedas.
- Atualização automática do ficheiro `stock.json` ao sair.
- Cálculo e apresentação do troco com moedas de €2, €1, 50c, 20c, etc.

---

## Como Usar
No terminal inserir:
```
python3 vendingMachine.py stock.json
```

## Exemplo de Uso

```
maq: 2025-05-25, stock carregado. Pronto para atender pedidos.

>> LISTAR

Código | Produto               | Quantidade | Preço
-------+------------------------+------------+-------
A01    | Água 0.5L              | 9          | 0.70€
B02    | Coca-Cola 33cl         | 8          | 1.00€
C03    | Sumo de Laranja        | 5          | 1.20€
D04    | Snack Bolacha          | 6          | 0.85€
E05    | Pastilha elástica      | 20         | 0.30€
>> MOEDA 1e, 20c, 20c .
Saldo atual: 1.40€
>> SELECIONAR A01
Produto 'Água 0.5L' dispensado. Saldo restante: 0.70€
>> LISTAR

Código | Produto               | Quantidade | Preço
-------+------------------------+------------+-------
A01    | Água 0.5L              | 8          | 0.70€
B02    | Coca-Cola 33cl         | 8          | 1.00€
C03    | Sumo de Laranja        | 5          | 1.20€
D04    | Snack Bolacha          | 6          | 0.85€
E05    | Pastilha elástica      | 20         | 0.30€
>> SAIR
maq: Pode retirar o troco: 1x 50c, 1x 20c
maq: Até à próxima!
```