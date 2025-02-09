from tabulate import tabulate

class Registradores_Segmento:

    def __init__(self,cs,ss,ds,es):
        self.linhas = ["CS", "SS", "DS", "ES","FS","GS"]
        self.colunas = ["16 BITS"]
        self.matriz = [[0] * len(self.colunas) for _ in range(len(self.linhas))]
        
        self.matriz[0][0] = cs
        self.matriz[1][0] = ss
        self.matriz[2][0] = ds
        self.matriz[3][0] = es
        self.matriz[4][0] = es
        self.matriz[5][0] = es
    
    def set_valor(self, linha, coluna, valor):

        if linha in self.linhas and coluna in self.colunas:
            i = self.linhas.index(linha)
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

        print(tabulate(self.matriz, headers=self.colunas, showindex=self.linhas, tablefmt="grid"))