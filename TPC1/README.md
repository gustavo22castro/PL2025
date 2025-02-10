# Criação de um somador de numeros em string # Somador On/Off
## Gustavo Castro, A100482

## Descrição
O programa lê uma String que contem números e substrings, sendo elas 'on', 'off' e '=' e realiza a soma dos números conforme o estado do somador.

## Funcionamento
- O programa inicia em modo de soma.
- As opções de estado e resultado são **on, off e =**, sendo que:
  - `on` ativa a soma.
  - `off` desativa a soma.
  - `=` exibe o resultado da soma acumulada até aquele momento.
- A soma ocorre apenas quando o estado está **ligado** (`on`). Caso esteja **desligado** (`off`), os números encontrados são ignorados.
- O texto de entrada é divido em substrings pelo espaço entre elas que são posteriormente processadas, ativando ou desativando a soma conforme os comandos e acumulando os valores corretamente.

## Exemplo de Uso
Entrada:
```plaintext 
"10 off 5 on 3 on 7 off 2 on 8 = off 4 on 2 ="
```
Saída esperada:
```plaintext 
11 2
```
