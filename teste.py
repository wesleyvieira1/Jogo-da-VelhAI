# Definição da classe Tabuleiro e JogadorIA
from random import randint
class Tabuleiro:
    DESCONHECIDO = 0
    JOGADOR_0 = 1
    JOGADOR_X = 4

    def __init__(self):
        self.matriz = [
            [Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO],
            [Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO],
            [Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO]
        ]

    def tem_campeao(self):
        # Verificar linhas
        for i in range(3):
            if self.matriz[i][0] == self.matriz[i][1] == self.matriz[i][2] != Tabuleiro.DESCONHECIDO:
                return self.matriz[i][0]
        
        # Verificar colunas
        for i in range(3):
            if self.matriz[0][i] == self.matriz[1][i] == self.matriz[2][i] != Tabuleiro.DESCONHECIDO:
                return self.matriz[0][i]
        
        # Verificar diagonais
        if self.matriz[0][0] == self.matriz[1][1] == self.matriz[2][2] != Tabuleiro.DESCONHECIDO:
            return self.matriz[0][0]
        if self.matriz[0][2] == self.matriz[1][1] == self.matriz[2][0] != Tabuleiro.DESCONHECIDO:
            return self.matriz[0][2]
        
        # Verifica se há empate
        for i in range(3):
            for j in range(3):
                if self.matriz[i][j] == Tabuleiro.DESCONHECIDO:
                    return Tabuleiro.DESCONHECIDO
        
        # Empate
        return Tabuleiro.OUTRO_TIPO

class JogadorIA:
    def __init__(self, tabuleiro: Tabuleiro, tipo: int):
        self.matriz = tabuleiro.matriz
        self.tipo = tipo

    def verificaLinha(self, linha, tipo):
        contagem_tipo = sum(1 for celula in self.matriz[linha] if celula == tipo)
        tem_vazio = Tabuleiro.DESCONHECIDO in self.matriz[linha]
        if contagem_tipo == 2 and tem_vazio:
            return (linha, self.matriz[linha].index(Tabuleiro.DESCONHECIDO))  # Retorna (linha, coluna)
        return None

    def verificaColuna(self, coluna: int, tipo: int):
        coluna_valores = [self.matriz[i][coluna] for i in range(3)]
        if coluna_valores.count(tipo) == 2 and coluna_valores.count(Tabuleiro.DESCONHECIDO) == 1:
            linha = coluna_valores.index(Tabuleiro.DESCONHECIDO)  # Pega o índice da linha
            return (linha, coluna)  # Retorna (linha, coluna)
        return None

    def verificaDiagonalPrincipal(self, tipo: int):
        diagonal = [self.matriz[i][i] for i in range(3)]
        if diagonal.count(tipo) == 2 and diagonal.count(Tabuleiro.DESCONHECIDO) == 1:
            index = diagonal.index(Tabuleiro.DESCONHECIDO)
            return (index, index)  # Coordenadas (linha, coluna)
        return None

    def verificaDiagonalSecundaria(self, tipo: int):
        diagonal = [self.matriz[i][2 - i] for i in range(3)]
        if diagonal.count(tipo) == 2 and diagonal.count(Tabuleiro.DESCONHECIDO) == 1:
            index = diagonal.index(Tabuleiro.DESCONHECIDO)
            return (index, 2 - index)  # Coordenadas (linha, coluna)
        return None

    def getJogada(self):
        # Verifica linha, coluna e diagonais usando regras semelhantes às anteriores
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

        # Se não houver jogada vencedora, retorna uma jogada aleatória
        lista = [(l, c) for l in range(3) for c in range(3) if self.matriz[l][c] == Tabuleiro.DESCONHECIDO]
        if len(lista) > 0:
            return lista[0]  # Escolhe o primeiro espaço vazio
        return None

    def regra1(self) -> (int, int):
        for l in range(3):
            jogada = self.verificaLinha(l, self.tipo)
            if jogada:
                return jogada
            jogada = self.verificaLinha(l, 3 - self.tipo)  # Bloqueio para oponentes
            if jogada:
                return jogada

        for c in range(3):
            jogada = self.verificaColuna(c, self.tipo)
            if jogada:
                return jogada
            jogada = self.verificaColuna(c, 3 - self.tipo)  # Bloqueio para oponentes
            if jogada:
                return jogada

        jogada = self.verificaDiagonalPrincipal(self.tipo)
        if jogada:
            return jogada
        jogada = self.verificaDiagonalPrincipal(3 - self.tipo)  # Bloqueio para oponentes
        if jogada:
            return jogada

        jogada = self.verificaDiagonalSecundaria(self.tipo)
        if jogada:
            return jogada
        jogada = self.verificaDiagonalSecundaria(3 - self.tipo)  # Bloqueio para oponentes
        if jogada:
            return jogada

        return None

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

    def regra3(self):
        if self.matriz[1][1] == Tabuleiro.DESCONHECIDO:
            return (1, 1)
        return None

    def regra4(self):
        cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        opostos = [(2, 2), (2, 0), (0, 2), (0, 0)]

        for i in range(4):
            if self.matriz[cantos[i][0]][cantos[i][1]] == 3 - self.tipo:
                return opostos[i]
        return None

    def regra5(self):
        cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for canto in cantos:
            if self.matriz[canto[0]][canto[1]] == Tabuleiro.DESCONHECIDO:
                return canto
        return None

    def regra6(self):
        lista_vazia = [(l, c) for l in range(3) for c in range(3) if self.matriz[l][c] == Tabuleiro.DESCONHECIDO]
        if lista_vazia:
            return lista_vazia[0]  # Escolhe o primeiro espaço vazio
        return None

    def criaDuasSequencias(self, linha: int, coluna: int) -> bool:
        if self.verificaLinha(linha, self.tipo) and self.verificaColuna(coluna, self.tipo):
            return True
        if (linha == coluna and self.verificaDiagonalPrincipal(self.tipo)) or (linha + coluna == 2 and self.verificaDiagonalSecundaria(self.tipo)):
            return True
        return False


# Testes com algumas jogadas
tabuleiro = Tabuleiro()
jogador_ia = JogadorIA(tabuleiro, Tabuleiro.JOGADOR_0)

# Jogadas consecutivas
print(jogador_ia.getJogada())  # Primeira jogada
print(jogador_ia.getJogada())  # Segunda jogada
print(jogador_ia.getJogada())  # Terceira jogada
print(tabuleiro.matriz)  # Verifica o estado atual do tabuleiro após as jogadas

# Jogada após criar sequências
tabuleiro.matriz = [
    [1, 1, 0],
    [0, 4, 0],
    [0, 0, 4]
]
print(jogador_ia.getJogada())  # Verifica como a IA joga após ter criado duas sequências

# Verificar vencedor (completa o exemplo anterior)
print(tabuleiro.tem_campeao())  # Verifica quem é o vencedor após
