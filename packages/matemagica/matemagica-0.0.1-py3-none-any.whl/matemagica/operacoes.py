def adicao(*parcelas):
    """Realiza todas as somas e retorna o resultado"""
    try:
        resultado = sum(parcelas)
    except:
        print('Argumento(s) inválido(s)! Insira apenas números!')
    else:
        return resultado


def subtracao(minuendo, *subtraendos):
    """Realiza todas as subtrações e retorna o resultado"""
    try:
        for subtraendo in subtraendos:
            minuendo -= subtraendo
    except:
        print('Argumento(s) inválido(s)! Insira apenas números!')
    else:
        resultado = minuendo
        return resultado


def multiplicao(*fatores):
    """Realiza todas as multiplicações e retorna o resultado"""
    try:
        resultado = 1
        for fator in fatores:
            resultado *= fator
    except:
        print('Argumento(s) inválido(s)! Insira apenas números!')
    else:
        return resultado


def divisao(dividendo, *divisores):
    """Realiza todas as divisões e retorna o resultado"""
    try:
        for divisor in divisores:
            dividendo /= divisor
    except:
        print('Argumento(s) inválido(s)! Insira apenas números!')
    else:
        resultado = dividendo
        return resultado


def divisao_inteira(dividendo: int, *divisores: int):
    """Realiza todas as divisões inteiras retorna o resultado e o resto, respectivamente"""
    try:
        for divisor in divisores:
            resto = dividendo
            dividendo //= divisor
            resto %= divisor
    except:
        print('Argumento(s) inválido(s)! Insira apenas números!')
    else:
        resultado = dividendo
        return resultado, resto


def potenciacao(base, expoente):
    """Realiza a potenciação e retorna o resultado"""
    try:
        resultado = base ** expoente
    except:
        print('Argumento(s) inválido(s)! Insira apenas números!')
    else:
        return resultado


def radiciacao(radicando, indice):
    """Realiza a radiciação e retorna o resultado"""
    try:
        resultado = radicando ** (1/indice)
    except:
        print('Argumento(s) inválido(s)! Insira apenas números!')
    else:
        return resultado
