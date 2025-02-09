from tabulate import tabulate
from Reg_Sel_Segmentos import Registradores_Segmento
class Descritores_Segmento:
    
    def __init__(self, reg_seletor_seg: Registradores_Segmento):
        self.linhas = ["cs","ss","ds","es"]
        self.colunas = ["SELETOR","END. BASE DO SEGMENTO","END. LIMITE", "DIREITO DE ACESSO"]
        self.matriz = [[0] * len(self.colunas) for _ in range(len(self.linhas))]
        
        self.matriz[0][0] = reg_seletor_seg.get_valor("CS","16 BITS")
        self.matriz[1][0] = reg_seletor_seg.get_valor("SS","16 BITS")
        self.matriz[2][0] = reg_seletor_seg.get_valor("DS","16 BITS")
        self.matriz[3][0] = reg_seletor_seg.get_valor("ES","16 BITS")

    def set_valor(self,seletor, endbase,endlimite,diracess):

        self.seletor = seletor
        self.endbase = endbase
        self.endlimite = endlimite
        self.diracess = diracess
         
        if coluna in self.colunas:
            i = self.linhas.index(self.linhas.len()-1)
            j = self.colunas.index(coluna)
            self.matriz[i][j] = valor
        else:
            print("Erro: Linha ou coluna inválida!")
    
    def get_valor(self, linha, coluna):
        
        if linha in self.linhas and coluna in self.colunas:
            i = self.linhas.index(linha)
            j = self.colunas.index(coluna)
            return self.matriz[i][j]
            
        else:
            print("Erro: Linha ou coluna inválida!")
            return None
        
    def print_matriz(self):

        print(tabulate(self.matriz, headers=self.colunas, tablefmt="grid"))
        self.linhas.append("")
