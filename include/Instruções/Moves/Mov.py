from Reg_Gerais import Registradores_Gerais
from Descritor_segmento import Descritores_Segmento
from EndereçoLinear import enderecamento_linear


def mov(destino, origem, memoria, registradores):
    if isinstance(destino, tuple):  # Se for memória
        endereco = enderecamento_linear(*destino)
        memoria.escrever(endereco, origem)
    elif isinstance(origem, tuple):  # Se for leitura de memória
        endereco = enderecamento_linear(*origem)
        valor = memoria.ler(endereco)
        registradores.set_valor(destino, "16 BITS", valor)
    else:  # Se for entre registradores
        registradores.set_valor(destino, "16 BITS", origem)

