from include.Tabelas.Descritor_Segmento import Descritores_Segmento
from include.Tabelas.Reg_Deslocamento import Registradores_Deslocamento
from include.Tabelas.Reg_Gerais import Registradores_Gerais
from include.Tabelas.Reg_Sel_Segmentos import Registradores_Segmento

descri_seg = Descritores_Segmento()
reg_deslocamento = Registradores_Deslocamento()
reg_gerais = Registradores_Gerais()
reg_seletor_seg = Registradores_Segmento()

    
def print_tabelas():
    descri_seg.print_matriz()
    reg_deslocamento.print_matriz()
    reg_gerais.print_matriz()
    reg_seletor_seg.print_matriz()   

