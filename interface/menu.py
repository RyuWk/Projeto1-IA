import sys

import pygame

from interface.interface import (
    BRANCO,
    COR_BORDA,
    COR_FUNDO,
    COR_PRIMARIA,
    COR_TEXTO,
    COR_TEXTO_MUTED,
    COR_VERDE,
    desenhar_card,
    fonte,
)

# Cores da Interface (Seguindo padrão de legibilidade e bom contraste)
COR_HOVER_CLARO = (239, 246, 255) # Fundo azulado claro ao passar o mouse
COR_HOVER_VERDE = (5, 150, 105)

# Medidas do card central do menu
LARGURA_CARD = 760
ALTURA_CARD = 600
PADDING = 48

class MenuInicial:
    def __init__(self, largura, altura):
        pygame.init()
        pygame.font.init()

        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Combate à Dengue - Menu Inicial")

        # Fontes grandes e legíveis para garantir acessibilidade
        self.fonte_titulo = fonte(34, True)
        self.fonte_subtitulo = fonte(18, True)
        self.fonte_opcao = fonte(17, True)
        self.fonte_texto = fonte(16)

        # Configurações selecionadas (Padrão)
        self.algoritmos = ["BFS (Largura)", "DFS (Profundidade)", "Gulosa", "A*"]
        self.cenarios = ["Cenário 1 (Pequeno)", "Cenário 2 (Médio)", "Cenário 3 (Complexo)"]

        self.algoritmo_idx = 0  # Padrão: BFS
        self.cenario_idx = 0     # Padrão: Cenário 1

        # Retorno das configurações
        self.iniciar_simulacao = False

    def desenhar_botao(self, texto, rect, ativo=False, hover=False):
        """Botão de opção: preenchido em azul quando selecionado, contornado caso contrário."""
        if ativo:
            pygame.draw.rect(self.tela, COR_PRIMARIA, rect, border_radius=10)
            cor_texto = BRANCO
        else:
            pygame.draw.rect(self.tela, COR_HOVER_CLARO if hover else BRANCO, rect, border_radius=10)
            pygame.draw.rect(self.tela, COR_PRIMARIA if hover else COR_BORDA, rect, width=2, border_radius=10)
            cor_texto = COR_TEXTO

        surf_texto = self.fonte_opcao.render(texto, True, cor_texto)
        self.tela.blit(surf_texto, surf_texto.get_rect(center=rect.center))

        return rect

    def renderizar(self):
        self.tela.fill(COR_FUNDO)

        rect_card = pygame.Rect(0, 0, LARGURA_CARD, ALTURA_CARD)
        rect_card.center = (self.largura // 2, self.altura // 2)
        desenhar_card(self.tela, rect_card, raio=20)

        x = rect_card.x + PADDING
        largura_util = LARGURA_CARD - 2 * PADDING
        centro_x = rect_card.centerx

        # Título do Jogo Educacional / Simulador
        titulo = self.fonte_titulo.render("Agente de Combate à Dengue", True, COR_TEXTO)
        subtitulo = self.fonte_texto.render("Selecione as configurações do cenário e do agente", True, COR_TEXTO_MUTED)

        self.tela.blit(titulo, titulo.get_rect(center=(centro_x, rect_card.y + 64)))
        self.tela.blit(subtitulo, subtitulo.get_rect(center=(centro_x, rect_card.y + 104)))
        pygame.draw.line(self.tela, COR_BORDA, (x, rect_card.y + 136), (x + largura_util, rect_card.y + 136))

        pos_mouse = pygame.mouse.get_pos()
        self.botoes_algoritmo = []
        self.botoes_cenario = []

        # 1. Seleção de Algoritmo (grade 2x2)
        y = rect_card.y + 164
        lbl_alg = self.fonte_subtitulo.render("1. Escolha o Algoritmo de Busca", True, COR_TEXTO)
        self.tela.blit(lbl_alg, (x, y))

        espaco = 16
        largura_alg = (largura_util - espaco) // 2
        for i, alg in enumerate(self.algoritmos):
            rect = pygame.Rect(
                x + (i % 2) * (largura_alg + espaco),
                y + 40 + (i // 2) * (52 + 12),
                largura_alg,
                52,
            )
            b_rect = self.desenhar_botao(
                alg, rect, ativo=(i == self.algoritmo_idx), hover=rect.collidepoint(pos_mouse)
            )
            self.botoes_algoritmo.append((b_rect, i))

        # 2. Seleção de Cenário (uma linha com três opções)
        y = rect_card.y + 340
        lbl_cen = self.fonte_subtitulo.render("2. Escolha o Cenário (Mapa)", True, COR_TEXTO)
        self.tela.blit(lbl_cen, (x, y))

        largura_cen = (largura_util - 2 * espaco) // 3
        for i, cen in enumerate(self.cenarios):
            rect = pygame.Rect(x + i * (largura_cen + espaco), y + 40, largura_cen, 52)
            b_rect = self.desenhar_botao(
                cen, rect, ativo=(i == self.cenario_idx), hover=rect.collidepoint(pos_mouse)
            )
            self.botoes_cenario.append((b_rect, i))

        # 3. Botão Iniciar
        rect_iniciar = pygame.Rect(0, 0, 300, 60)
        rect_iniciar.center = (centro_x, rect_card.bottom - 72)
        is_hover_iniciar = rect_iniciar.collidepoint(pos_mouse)

        pygame.draw.rect(self.tela, COR_HOVER_VERDE if is_hover_iniciar else COR_VERDE, rect_iniciar, border_radius=14)
        txt_iniciar = fonte(20, True).render("INICIAR MISSÃO", True, BRANCO)
        self.tela.blit(txt_iniciar, txt_iniciar.get_rect(center=rect_iniciar.center))

        self.btn_iniciar = rect_iniciar

    def executar(self):
        clock = pygame.time.Clock()

        while not self.iniciar_simulacao:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Clique em Algoritmos
                    for rect, idx in self.botoes_algoritmo:
                        if rect.collidepoint(event.pos):
                            self.algoritmo_idx = idx

                    # Clique em Cenários
                    for rect, idx in self.botoes_cenario:
                        if rect.collidepoint(event.pos):
                            self.cenario_idx = idx

                    # Clique em Iniciar
                    if self.btn_iniciar.collidepoint(event.pos):
                        self.iniciar_simulacao = True

            self.renderizar()
            pygame.display.flip()
            clock.tick(30)

        return {
            "algoritmo": self.algoritmos[self.algoritmo_idx],
            "cenario_idx": self.cenario_idx
        }
