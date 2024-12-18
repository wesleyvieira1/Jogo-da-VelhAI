# -*- coding: utf-8 -*-
from tabuleiro_screen import TabuleiroScreen
from tabuleiro import Tabuleiro
from jogador import Jogador
from jogador_ia import JogadorIA
from jogador_humano import JogadorHumano

class JogoVelha:
    def __init__(self):
        self.screen = TabuleiroScreen()
        self.tabuleiro = Tabuleiro()
        
        # Jogadores
        self.jogadores = [
            JogadorIA(self.tabuleiro, Tabuleiro.JOGADOR_0),
            JogadorHumano(self.tabuleiro, self.screen.buttons, Tabuleiro.JOGADOR_X)
        ]
        self.id_jogador_corrente = 0
        self.jogador_corrente: Jogador = self.jogadores[self.id_jogador_corrente]
        
    def troca_jogador(self):
        self.id_jogador_corrente = (self.id_jogador_corrente + 1) % 2
        self.jogador_corrente = self.jogadores[self.id_jogador_corrente]
        
    def wait_quit_event(self):
        self.screen.wait_quit_event()
    
    def acabou_jogo(self):
        resultado = self.tabuleiro.tem_campeao()
        
        if resultado == Tabuleiro.JOGADOR_X:
            self.screen.resultado_txt = "X vencedor!"
            return True
            
        if resultado == Tabuleiro.JOGADOR_0:
            self.screen.resultado_txt = "O vencedor!"
            return True
        
        return False
                              
    def start(self):
        acabou_jogo = False
        contador = 0
        
        while True:
            x, y = self.jogador_corrente.getJogada()
            self.screen.update_text_button(x, y, self.jogador_corrente.tipo)
            self.tabuleiro.matriz[x][y] = self.jogador_corrente.tipo
                                
            contador += 1
            
            if self.acabou_jogo():
                self.screen.desenha_tabuleiro()
                break
            
            if contador == 9:
                self.screen.resultado_txt = "Deu velha!"
                self.screen.desenha_tabuleiro()
                break
            
            self.screen.desenha_tabuleiro()
            self.troca_jogador()
    

    def testa_jogada_ia(self):
        resultado = self.tabuleiro.tem_campeao()

        if resultado == Tabuleiro.DESCONHECIDO:
            for i in range(3):
                for j in range(3):
                    if self.tabuleiro.matriz[i][j] == Tabuleiro.DESCONHECIDO:
                        self.tabuleiro.matriz[i][j] = Tabuleiro.JOGADOR_0  # Simulando a IA fazendo um movimento
                        if self.tabuleiro.tem_campeao() == Tabuleiro.JOGADOR_0:
                            return (i, j)  # Retorna a jogada bloqueadora
                        self.tabuleiro.matriz[i][j] = Tabuleiro.DESCONHECIDO
        return None  # Nenhuma jogada foi bloqueada

