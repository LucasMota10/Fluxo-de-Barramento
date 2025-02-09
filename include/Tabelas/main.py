from Descritor_Segmento import Descritores_Segmento
from Reg_Deslocamento import Registradores_Deslocamento
from Reg_Gerais import Registradores_Gerais
from Reg_Sel_Segmentos import Registradores_Segmento


# Instanciação dos Registradores e Tabela de Descritores

def verifica_tamanho(x):
    if len(x) != 4 or max(x) > "f" :
        print("Erro! Valor não válido, tente novamente")
        return False
    else:
        return True

cs = ss = ds = es = ""

def menu():
    print("Olá usuário, Vamos começar o fluxo!")
    print("Antes de tudo, vamos incializar os registradores")
    print("Insira o Valor desejado para os registradores de seguimento abaixo:")
    print("OBS: Apenas 4 Bits em Hexadecimal")
        
    while True:  
        global cs
        cs = input("Registrador CS: ")
        if verifica_tamanho(cs):
            break
    
    while True:  
        global ss
        ss = input("Registrador SS: ")
        if verifica_tamanho(ss):
            break
    while True:  
        global ds
        ds = input("Registrador DS: ")
        if verifica_tamanho(ds):
            break
    while True:  
        global es
        es = input("Registrador ES: ")
        if verifica_tamanho(es):
            break
def print_tabelas():
    descri_seg.print_matriz()
    reg_deslocamento.print_matriz()
    reg_gerais.print_matriz()
    reg_seletor_seg.print_matriz() 


menu()
reg_deslocamento = Registradores_Deslocamento()
reg_gerais = Registradores_Gerais()
reg_seletor_seg = Registradores_Segmento(cs,ss,ds,es)
descri_seg = Descritores_Segmento(reg_seletor_seg)

    
  

print_tabelas()

