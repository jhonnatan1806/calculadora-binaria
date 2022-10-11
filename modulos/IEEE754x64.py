from modulos.binario import Binario
from modulos.fraccionario import Fraccionario

class IEEE754x64:

    def __init__(self):
        pass

    # =======================================================
    # Algoritmo de base 10 a base 2
    # =======================================================
    
    def dec_bin(self,numero):
        # P1 Identificar el Signo
        # 0 = positivo & 1 = negativo
        signo = '0' if numero >= 0 else '1'
        # P2 Convertir en Numero en binario Fraccionario
        # binario[0] = parte entera binario[1] = parte fraccionaria
        b_fracionado = Fraccionario().dec_bin(abs(numero),52)
        binario = b_fracionado.split('.')
        # P3 Identificar el Exponente y el tipo de numero
        # Se identifica si tiene parte entera o no
        if int(binario[0]) > 0:
            # Se le suma exponentes -1 + 1023
            palabra = str(int(binario[0]))
            exp_dec = len(palabra) - 1 + 1023
            exp_bin = Binario().dec_bin(exp_dec)
        else:
            # Se le resta 1024 - exponentes [VERIFICAR]
            exp_dec = binario[1].index('1') + 2
            exp_bin = Binario().dec_bin(1024 - exp_dec)
        # Se empaqueta en 11 bits
        exponente = '0'*(11-len(exp_bin)) + exp_bin
        # P4 Identificar la Mantisa
        if int(binario[0]) > 0:
            pos = binario[0].index('1')
            mantisa = binario[0][pos+1:] + binario[1]
        else:
            mantisa = binario[1][exp_dec:]
        bits = len(mantisa)
        if bits<52:
            mantisa = mantisa + '0'*(52-bits)
        else:
            mantisa = mantisa[:52]
        # P5 Unir las tres partes
        return signo + exponente + mantisa

    # =======================================================
    # Algoritmo de base 2 a base 10
    # =======================================================

    def bin_dec(self,palabra):
        if len(palabra)<64:
            fix = 64-len(palabra)
            palabra = palabra + '0'*fix
        # P1. Separar las partes 
        b_signo = palabra[0]
        b_exponente = palabra[1:12]
        b_mantisa = palabra[12:]
        # P2. Identificar el Signo
        signo = 1 if b_signo == '0' else -1
        # P3. Identificar el Exponente y el tipo de numero (Infinito, Fraccionario naturalizado o desnaturalizado, cero)
        exponente = Binario().bin_dec(b_exponente) - 1023
        # Identificar la Mantisa y convertir el numero en Binario Fraccionario de punto fijo
        if exponente == 1024:
            return 'infinito' if signo == 1 else '-infinito'
        elif exponente == -1023:
            return 0
        else:
            # Es normalizada 
            if exponente < 0:
                b_frac = '0.' + '0'*exponente + '1' + b_mantisa
            elif exponente >=1 or exponente <= 52:
                b_frac = '1' + b_mantisa[:exponente] + '.' + b_mantisa[exponente:]
            else:
                faltante = exponente - 52
                b_frac = '1' + b_mantisa + '0'*faltante + '0.0'
            # Convertir el Binario Fraccionario de punto fijo a Decimal
            n_base10 = Fraccionario().bin_dec(b_frac)
        return round(n_base10*signo,8)
        