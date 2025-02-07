from tabulate import tabulate

class Descritores_Segmento:
    
    def __init__(self):
        self.linhas = [""]
        self.colunas = ["SELETOR","END. BASE DO SEGMENTO","END. LIMITE", "DIREITO DE ACESSO"]
        self.matriz = [[0] * len(self.colunas) for _ in range(len(self.linhas))]

    def set_valor(self,coluna, valor):

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
