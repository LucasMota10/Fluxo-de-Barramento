from tabulate import tabulate

class Registradores_Segmento:

    def __init__(self):
        self.__linhas = ["CS", "SS", "DS", "ES","FS","GS"]
        self.__colunas = ["16 BITS"]
        self.__matriz = [[0] * len(self.__colunas) for _ in range(len(self.__linhas))]
        
        self.__matriz[0][0] = "A000"
        self.__matriz[1][0] = "B000"
        self.__matriz[2][0] = "C000"
        self.__matriz[3][0] = "D000"
        self.__matriz[4][0] = "E000"
        self.__matriz[5][0] = "F000"
    
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

        print(tabulate(self.__matriz, headers=self.__colunas, showindex=self.__linhas, tablefmt="grid"))