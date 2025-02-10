
def onoff(seqDigitos):
    soma = 0
    mode = True
    entradas = seqDigitos.split()

    for entrada in entradas:
        if entrada.lower() == 'on':
            mode = True
        elif entrada.lower() == 'off':
            mode = False
        elif entrada.lower() == '=':
            print(soma)
        elif entrada.isdigit() and mode:
            soma += int(entrada)

        