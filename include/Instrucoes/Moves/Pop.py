from Reg_Gerais import Registradores_Gerais
from Reg_Sel_Segmento import Registradores_Segmento
from Reg_Deslocamento import Registradores_Deslocamento
from EndereçoLinear import enderecamento_linear

def pop(destino, memoria, registradores_deslocamento, registradores_gerais):
    esp = registradores_deslocamento.get_valor("ESP", "32 BITS")
    valor = memoria.ler(esp)
    if isinstance(destino, tuple):  # Se for armazenar na memória
        endereco = enderecamento_linear(*destino)
        memoria.escrever(endereco, valor)
    else:
        registradores_gerais.set_valor(destino, "16 BITS", valor)
    registradores_deslocamento.set_valor("ESP", "32 BITS", esp + 2)

