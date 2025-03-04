# Conversor de Markdown para HTML

Este programa converte um ficheiro Markdown em HTML utilizando expressões regulares. Ele trata os seguintes elementos:

## Funcionalidades Implementadas

### Cabeçalhos

Os cabeçalhos Markdown são convertidos em títulos HTML:

```python
# Título principal -> <h1></h1>
## Subtítulo -> <h2></h2>
### Sub-subtítulo -> <h3></h3>
```

### Texto em Negrito

Palavras ou frases entre `**` ficam entre `<b>` e `</b>`:

```python
**negrito** -> <b>negrito</b>
```

### Texto em Itálico

Palavras ou frases entre `*` ficam entre `<i>` e `</i>`:

```python
*itálico* -> <i>itálico</i>
```

### Listas Ordenadas

Listas ordenadas em Markdown são transformadas em listas `<ol>` em HTML:

```python
1. Item 1
2. Item 2
3. Item 3
```

Vira:

```html
<ol>
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
</ol>
```

### Links

Os links em Markdown são convertidos em links HTML:

```python
[Texto do link](http://exemplo.com) -> <a href="http://exemplo.com">Texto do link</a>
```

### Imagens

Imagens em Markdown são transformadas em `<img>`:

```python
![Alt text](imagem.jpg) -> <img src="imagem.jpg" alt="Alt text"/>
```

## Como Usar

1. Copie o código acima para um arquivo Python.
2. Execute a função `md_to_html()` passando um texto em Markdown como argumento.
3. O retorno será o equivalente em HTML.
