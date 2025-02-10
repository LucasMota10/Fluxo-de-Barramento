from Instrucoes.Moves.Mov import MOV
from Instrucoes.Arithmetic.Add import ADD
from Instrucoes.Compare.Cmp import CMP
from Instrucoes.Boolean.And import AND
from Instrucoes.Moves.Mov import MOV
from Instrucoes.Moves.Xchg import XCHG
from Instrucoes.Moves.Pop import POP
from Instrucoes.Moves.Push import PUSH
from Instrucoes.Arithmetic.Inc import INC
from Instrucoes.Compare.Jmp import JMP
from Instrucoes.Arithmetic.Sub import SUB

# Instanciação dos Registradores e Tabela de Descritores

# def verifica_tamanho(x):
#     if len(x) != 4 or max(x) > "f" :
#         print("Erro! Valor não válido, tente novamente")
#         return False
#     else:
#         return True

# cs = ss = ds = es = ""

# def menu():
#     print("Olá usuário, Vamos começar o fluxo!")
#     print("Antes de tudo, vamos incializar os registradores")
#     print("Insira o Valor desejado para os registradores de seguimento abaixo:")
#     print("OBS: Apenas 4 Bits em Hexadecimal")
        
#     while True:  
#         global cs
#         cs = input("Registrador CS: ")
#         if verifica_tamanho(cs):
#             break
    
#     while True:  
#         global ss
#         ss = input("Registrador SS: ")
#         if verifica_tamanho(ss):
#             break
#     while True:  
#         global ds
#         ds = input("Registrador DS: ")
#         if verifica_tamanho(ds):
#             break
#     while True:  
#         global es
#         es = input("Registrador ES: ")
#         if verifica_tamanho(es):
#             break
# def print_tabelas():
#     descri_seg.print_matriz()
#     reg_deslocamento.print_matriz()
#     reg_gerais.print_matriz()
#     reg_seletor_seg.print_matriz() 

#reg_deslocamento = Registradores_Deslocamento()
#reg_gerais = Registradores_Gerais()
#reg_seletor_seg = Registradores_Segmento(cs,ss,ds,es)
#descri_seg = Descritores_Segmento(reg_seletor_seg)

    
  

#print_tabelas()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def main():
    print("==============================================")
    print("Simulação de Instruções em Modo Protegido (32 bits)")
    print("==============================================\n")
    
    # 1. Leitura dos endereços base dos segmentos
    print("Informe os endereços BASE dos segmentos (use 8 dígitos hexadecimais, ex: 0x00000000):")
    code_base_str  = input("   - Endereço base do segmento de CÓDIGO: ").strip()
    data_base_str  = input("   - Endereço base do segmento de DADOS: ").strip()
    stack_base_str = input("   - Endereço base do segmento de PILHA: ").strip()
    
    try:
        code_base  = int(code_base_str, 16)
        data_base  = int(data_base_str, 16)
        stack_base = int(stack_base_str, 16)
    except ValueError:
        print("Erro: Certifique-se de informar os endereços no formato hexadecimal (ex: 0x00000000).")
        return
    
    # O endereço final do segmento de código é um a menos que o endereço base do segmento de dados.
    # O endereço final do segmento de dados é um a menos que o endereço base do segmento de pilha.
    code_limit = data_base - 1
    data_limit = stack_base - 1
    stack_limit_str = input("Digite o ENDEREÇO FINAL do segmento de PILHA (ex: 0xFFFFFFFF): ").strip()
    try:
        stack_limit = int(stack_limit_str, 16)
    except ValueError:
        print("Erro: Endereço final do segmento de pilha em formato inválido.")
        return

    print("\n==============================================")
    print("Agora, informe os SELETORES e os DIREITOS DE ACESSO de cada segmento:")
    cs_selector = input("   - Seletor do segmento de CÓDIGO (CS): ").strip()
    cs_access   = input("   - Direito de acesso do segmento de CÓDIGO (CS): ").strip()
    
    ds_selector = input("   - Seletor do segmento de DADOS (DS): ").strip()
    ds_access   = input("   - Direito de acesso do segmento de DADOS (DS): ").strip()
    
    ss_selector = input("   - Seletor do segmento de PILHA (SS): ").strip()
    ss_access   = input("   - Direito de acesso do segmento de PILHA (SS): ").strip()
    
    # 2. Criação e exibição da tabela de descritores
    print("\n==============================================")
    print("Tabela de Descritores de Segmentos:")
    print("|  Seletor  |   Endereço BASE do Segmento   |  Endereço LIMITE do Segmento  |  Direito de Acesso  |")
    print("-" * 85)
    descriptors = [
        {"Seletor": cs_selector, "Base": code_base_str,  "Limite": hex(code_limit),  "Acesso": cs_access},
        {"Seletor": ds_selector, "Base": data_base_str,  "Limite": hex(data_limit),  "Acesso": ds_access},
        {"Seletor": ss_selector, "Base": stack_base_str, "Limite": hex(stack_limit), "Acesso": ss_access}
    ]
    for d in descriptors:
        print(f"| {d['Seletor']:^9} | {d['Base']:^27} | {d['Limite']:^29} | {d['Acesso']:^19} |")
    
    # 3. Seleção da instrução a ser simulada
    print("\n==============================================")
    instr = input("Digite a instrução a ser simulada (ex: MOV): ").strip().upper()
    match instr:
        case "MOV":
            MOV(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector)
        case "ADD":
            ADD(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector)
        case "CMP":
            CMP(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector)
        case "AND":
            AND(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector)
        case "PUSH":
            PUSH(code_base, code_limit, stack_base, stack_limit, cs_selector, ss_selector)
        case "POP":
            POP(code_base, code_limit, stack_base, stack_limit, cs_selector, ss_selector)
        case "XCHG":
            XCHG(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector)
        case "INC":
            INC(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector)
        case "JMP":
            JMP(code_base, code_limit, cs_selector)
        case "SUB":
            SUB(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector)
        case _:
            print("Instrução não suportada.")
            return
    
    # 4. Informações para o cálculo de endereços lógicos e o fluxo da instrução
    
    
if __name__ == "__main__":
    main()