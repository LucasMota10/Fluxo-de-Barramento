from tabulate import tabulate

class Registradores_Gerais:

    def __init__(self):
        self.linhas = ["EAX", "EBX", "ECX", "EDX"]
        self.colunas = ["16 BITS", "high - 8 BITS", "low - 8 BITS"]
        self.matriz = [[0] * len(self.colunas) for _ in range(len(self.linhas))]

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
