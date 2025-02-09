from Reg_Gerais import Registradores_Gerais
from Reg_Sel_Segmento import Registradores_Segmento
from Reg_Deslocamento import Registradores_Deslocamento
from EndereçoLinear import enderecamento_linear

def push(origem, memoria, registradores_deslocamento):
    esp = registradores_deslocamento.get_valor("ESP", "32 BITS") - 2
    registradores_deslocamento.set_valor("ESP", "32 BITS", esp)
    if isinstance(origem, tuple):  # Se for um endereço de memória
        endereco = enderecamento_linear(*origem)
        valor = memoria.ler(endereco)
    else:
        valor = origem
    memoria.escrever(esp, valor)


