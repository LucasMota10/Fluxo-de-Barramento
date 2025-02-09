from Reg_Gerais import Registradores_Gerais
from EndereçoLinear import enderecamento_linear

def xchg(op1, op2, memoria, registradores):
    if isinstance(op1, tuple):  # Se op1 for memória
        endereco1 = enderecamento_linear(*op1)
        valor1 = memoria.ler(endereco1)
    else:
        valor1 = registradores.get_valor(op1, "16 BITS")

    if isinstance(op2, tuple):  # Se op2 for memória
        endereco2 = enderecamento_linear(*op2)
        valor2 = memoria.ler(endereco2)
    else:
        valor2 = registradores.get_valor(op2, "16 BITS")

    if isinstance(op1, tuple):
        memoria.escrever(endereco1, valor2)
    else:
        registradores.set_valor(op1, "16 BITS", valor2)

    if isinstance(op2, tuple):
        memoria.escrever(endereco2, valor1)
    else:
        registradores.set_valor(op2, "16 BITS", valor1)

