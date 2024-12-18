# -*- coding: utf-8 -*-
from random import randint
from jogador import Jogador
from tabuleiro import Tabuleiro

class JogadorIA(Jogador):
    def __init__(self, tabuleiro: Tabuleiro, tipo: int):
        self.matriz = tabuleiro.matriz
        self.tipo = tipo

    # Verifica se a linha tem duas marcações do tipo passado e uma célula desconhecida
    def verificaLinha(self, linha, tipo):
        contagem_tipo = sum(1 for celula in self.matriz[linha] if celula == tipo)
        tem_vazio = Tabuleiro.DESCONHECIDO in self.matriz[linha]
        if contagem_tipo == 2 and tem_vazio:
            return (linha, self.matriz[linha].index(Tabuleiro.DESCONHECIDO))
        return None

    # Verifica se a coluna tem duas marcações do tipo passado e uma célula desconhecida
    def verificaColuna(self, coluna: int, tipo: int):
        coluna_valores = [self.matriz[i][coluna] for i in range(3)]
        if coluna_valores.count(tipo) == 2 and coluna_valores.count(Tabuleiro.DESCONHECIDO) == 1:
            linha = coluna_valores.index(Tabuleiro.DESCONHECIDO) 
            return (linha, coluna) 
        return None

    # Verifica se a diagonal principal tem duas marcações do tipo passado e uma célula desconhecida
    def verificaDiagonalPrincipal(self, tipo: int):
        diagonal = [self.matriz[i][i] for i in range(3)]
        if diagonal.count(tipo) == 2 and diagonal.count(Tabuleiro.DESCONHECIDO) == 1:
            index = diagonal.index(Tabuleiro.DESCONHECIDO)
            return (index, index) 
        return None

    # Verifica se a diagonal secundária tem duas marcações do tipo passado e uma célula desconhecida
    def verificaDiagonalSecundaria(self, tipo: int):
        diagonal = [self.matriz[i][2 - i] for i in range(3)]
        if diagonal.count(tipo) == 2 and diagonal.count(Tabuleiro.DESCONHECIDO) == 1:
            index = diagonal.index(Tabuleiro.DESCONHECIDO)
            return (index, 2 - index) 
        return None

    # R1 - Se você ou seu oponente tiver duas marcações em sequência, marque o quadrado restante.
    def regra1(self):
        # Verificar linhas, colunas e diagonais para o próprio jogador
        for i in range(3):
            resultado_linha = self.verificaLinha(i, self.tipo)
            if resultado_linha:
                return resultado_linha
            resultado_coluna = self.verificaColuna(i, self.tipo)
            if resultado_coluna:
                return resultado_coluna

        # Verificar diagonais
        resultado_diagonal_principal = self.verificaDiagonalPrincipal(self.tipo)
        if resultado_diagonal_principal:
            return resultado_diagonal_principal

        # Verificar diagonais
        resultado_diagonal_secundaria = self.verificaDiagonalSecundaria(self.tipo)
        if resultado_diagonal_secundaria:
            return resultado_diagonal_secundaria

        # Verificar linhas, colunas e diagonais para o oponente
        for i in range(3):
            resultado_linha = self.verificaLinha(i, Tabuleiro.JOGADOR_X)
            if resultado_linha:
                return resultado_linha
            resultado_coluna = self.verificaColuna(i, Tabuleiro.JOGADOR_X)
            if resultado_coluna:
                return resultado_coluna

        # Verificar diagonais
        resultado_diagonal_principal = self.verificaDiagonalPrincipal(Tabuleiro.JOGADOR_X)
        if resultado_diagonal_principal:
            return resultado_diagonal_principal
        # Verificar diagonais
        resultado_diagonal_secundaria = self.verificaDiagonalSecundaria(Tabuleiro.JOGADOR_X)
        if resultado_diagonal_secundaria:
            return resultado_diagonal_secundaria

        return None

    # R2 - Se houver uma jogada que crie duas sequências de duas marcações, use-a.
    def regra2(self):
        for l in range(3):
            for c in range(3):
                if self.matriz[l][c] == Tabuleiro.DESCONHECIDO:
                    self.matriz[l][c] = self.tipo  # Marca temporariamente
                    if self.criaDuasSequencias(l, c):
                        self.matriz[l][c] = Tabuleiro.DESCONHECIDO  # Desfaz a marcação
                        return (l, c)
                    self.matriz[l][c] = Tabuleiro.DESCONHECIDO  # Desfaz a marcação
        return None

    # R3 - Se o quadrado central estiver livre, marque-o
    def regra3(self):
        if self.matriz[1][1] == Tabuleiro.DESCONHECIDO:
            return (1, 1)
        return None

    # R4 - Se seu oponente tiver marcado um dos cantos, marque o canto oposto.
    def regra4(self):
        cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        opostos = [(2, 2), (2, 0), (0, 2), (0, 0)]  # Canto oposto correspondente
        for i in range(4):
            if self.matriz[cantos[i][0]][cantos[i][1]] == Tabuleiro.OUTRO_TIPO:
                return opostos[i]
        return None

    # R5 - Se houver um canto vazio, marque-o
    def regra5(self):
        cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for canto in cantos:
            if self.matriz[canto[0]][canto[1]] == Tabuleiro.DESCONHECIDO:
                return canto
        return None

    # R6 - Marque arbitrariamente um quadrado vazio.
    def regra6(self):
        lista_vazia = []
        for l in range(3):
            for c in range(3):
                if self.matriz[l][c] == Tabuleiro.DESCONHECIDO:
                    lista_vazia.append((l, c))
        if lista_vazia:
            return lista_vazia[randint(0, len(lista_vazia) - 1)]
        return None

    # Verifica se a jogada cria duas sequências de duas marcações
    def criaDuasSequencias(self, linha: int, coluna: int) -> bool:
        if self.verificaLinha(linha, self.tipo) and self.verificaColuna(coluna, self.tipo):
            return True
        if (linha == coluna and self.verificaDiagonalPrincipal(self.tipo)) or (linha + coluna == 2 and self.verificaDiagonalSecundaria(self.tipo)):
            return True
        return False

    # Retorna a jogada do jogador
    def getJogada(self):
        
        jogada = self.regra1()
        if jogada:
            return jogada
        
        jogada = self.regra2()
        if jogada:
            return jogada
        
        jogada = self.regra3()
        if jogada:
            return jogada
        
        jogada = self.regra4()
        if jogada:
            return jogada
        
        jogada = self.regra5()
        if jogada:
            return jogada
        
        jogada = self.regra6()
        if jogada:
            return jogada
        return None
