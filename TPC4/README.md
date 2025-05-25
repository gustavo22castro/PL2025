# TPC4 – Analisador Léxico para Consultas do tipo SPARQL

## Autor
Gustavo Castro - A100482

## Objetivo

O trabalho consiste em construir um analisador léxico simples em Python que identifica os principais componentes de uma linguagem semelhante ao SPARQL. O objetivo é transformar uma consulta textual em unidades léxicas (tokens) classificadas por tipo.

---

## Exemplo de Entrada

```sparql
select ?nome ?desc where {
  ?s a dbo:MusicalArtist.
  ?s foaf:name "Chuck Berry"@en .
  ?w dbo:artist ?s.
  ?w foaf:name ?nome.
  ?w dbo:abstract ?desc
} LIMIT 1000
```
## Exemplo de Saida
```tex
Aviso: símbolo não reconhecido -> a
Tokens identificados:
RESERVADA    → SELECT
VARIAVEL     → ?nome
VARIAVEL     → ?desc
RESERVADA    → WHERE
DELIMITADOR  → {
VARIAVEL     → ?s
NOME_IRI     → dbo:MusicalArtist
DELIMITADOR  → .
VARIAVEL     → ?s
NOME_IRI     → foaf:name
CADEIA       → "Chuck Berry"@en
DELIMITADOR  → .
VARIAVEL     → ?w
NOME_IRI     → dbo:artist
VARIAVEL     → ?s
DELIMITADOR  → .
VARIAVEL     → ?w
NOME_IRI     → foaf:name
VARIAVEL     → ?nome
DELIMITADOR  → .
VARIAVEL     → ?w
NOME_IRI     → dbo:abstract
VARIAVEL     → ?desc
DELIMITADOR  → }
RESERVADA    → LIMIT
NUMERO       → 1000
```
## Tipos de Tokens
- RESERVADA — Palavras-chave como select, where, limit

- VAR — Variáveis iniciadas por ?

- NAMESPACE — URIs com prefixos dbo: ou foaf:

- TEXTO — Strings entre aspas, com possível tag de idioma (ex: @en)

- NUM — Números inteiros

- DELIM — Símbolos {, }, .

- INVALIDO — Qualquer símbolo não previsto (gera erro)

## Funcionamento
O programa contém um conjunto de expressões regulares para cada tipo de token. Utiliza a função ``re.finditer()`` para percorrer a string de entrada e identificar os elementos um a um. Os espaços são ignorados e símbolos inválidos provocam erro.

O resultado é uma lista de pares (valor, tipo), representando os tokens da consulta.

