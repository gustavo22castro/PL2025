# Análise de um dataset de obras musicais

## Gustavo Castro, A100482

## Descrição

Este programa em python tem como objetivo fazer o parsing de um ficheiro csv sem usar o modulo csv, organizar a informação processada e imprimi-la de acordo com o que é pedido no enunciado.

## Resultados Pretendidos

1. Lista ordenada alfabeticamente dos compositores musicais;
2. Distribuição das obras por período: quantas obras catalogadas em cada período;
3. Dicionário em que a cada período está a associada uma lista alfabética dos títulos das obras desse período.

## Funcionamento

- Abertura e escrita numa string de todos os caracteres do ficheiro
- Parsing Manual do CSV (parse_csv)
  - Percorre o Conteúdo do Arquivo Caractere por Caractere seguindo as seguintes regras:
    - Aspas ("): Alterna o estado de dentro_aspas (True ou False).
    - Quebra de Linha (\n):
        **Se estiver fora das aspas:**
        Finaliza a linha atual (current_row).
        Armazena-a em rows.
        Reinicia current_row e field.
        Separador de Campo (;):

        **Se estiver fora das aspas:**
        Adiciona o campo atual à linha.
        Reinicia o field.

    - Outros Caracteres: Adiciona o caractere ao field atual.
    - Finaliza a Última Linha e Campo (caso o arquivo não termine com uma quebra de linha):
  - Retorna a linha em lista de parametros já nos seus respetivos tipos
- Analise de obras musicais
  1. Cria a lista de compositores unicos e ordena-a para que possa ser impressa

  2. Cria um Dicionário (obras_por_periodo):
     - Chave -> período
     - Valor -> lista de obras pertencentes a esse período

  3. Ordena as Obras Alfabeticamente Dentro de Cada Período aproveitando o dicionario criado ateriormente:
     - Usa a função sorted() para ordenar primeiro os períodos e depois as obras pelo nome.
