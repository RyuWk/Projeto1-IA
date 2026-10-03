import sys

import pygame

# Cores da Interface (Seguindo padrão de legibilidade e bom contraste)
COR_FUNDO = (245, 247, 250)
COR_TEXTO = (30, 41, 59)
COR_PRIMARIA = (37, 99, 235)      # Azul principal
COR_HOVER = (29, 78, 216)         # Azul escuro ao passar o mouse
COR_SELECIONADO = (16, 185, 129)  # Verde destaque
COR_BORDAS = (203, 213, 225)

class MenuInicial:
    def __init__(self, largura, altura):
        pygame.init()
        pygame.font.init()

        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Combate à Dengue - Menu Inicial")

        # Fontes grandes e legíveis para garantir acessibilidade
        self.fonte_titulo = pygame.font.SysFont("Arial", 28, bold=True)
        self.fonte_subtitulo = pygame.font.SysFont("Arial", 20, bold=True)
        self.fonte_opcao = pygame.font.SysFont("Arial", 16)

        # Configurações selecionadas (Padrão)
        self.algoritmos = ["BFS (Largura)", "DFS (Profundidade)", "Gulosa", "A*"]
        self.cenarios = ["Cenário 1 (Pequeno)", "Cenário 2 (Médio)", "Cenário 3 (Complexo)"]

        self.algoritmo_idx = 0  # Padrão: A*
        self.cenario_idx = 0     # Padrão: Cenário 1

        # Retorno das configurações
        self.iniciar_simulacao = False

    def desenhar_botao(self, texto, x, y, w, h, ativo=False, hover=False):
        cor_fundo = COR_SELECIONADO if ativo else (COR_HOVER if hover else COR_PRIMARIA)
        rect = pygame.Rect(x, y, w, h)

        pygame.draw.rect(self.tela, cor_fundo, rect, border_radius=8)
        pygame.draw.rect(self.tela, COR_BORDAS, rect, width=2, border_radius=8)

        surf_texto = self.fonte_opcao.render(texto, True, (255, 255, 255))
        rect_texto = surf_texto.get_rect(center=rect.center)
        self.tela.blit(surf_texto, rect_texto)

        return rect

    def renderizar(self):
        self.tela.fill(COR_FUNDO)

        # Título do Jogo Educacional / Simulador
        titulo = self.fonte_titulo.render("Agente de Combate à Dengue", True, COR_TEXTO)
        subtitulo = self.fonte_opcao.render("Selecione as configurações do cenário e do agente", True, (100, 116, 139))

        self.tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 40))
        self.tela.blit(subtitulo, (self.largura // 2 - subtitulo.get_width() // 2, 80))

        pos_mouse = pygame.mouse.get_pos()
        self.botoes_algoritmo = []
        self.botoes_cenario = []

        # 1. Seleção de Algoritmo
        lbl_alg = self.fonte_subtitulo.render("1. Escolha o Algoritmo de Busca:", True, COR_TEXTO)
        self.tela.blit(lbl_alg, (80, 140))

        y_alg = 180
        for i, alg in enumerate(self.algoritmos):
            x_alg = 80 + (i % 2) * 320
            if i == 2:
                y_alg += 60

            rect = pygame.Rect(x_alg, y_alg, 300, 45)
            is_hover = rect.collidepoint(pos_mouse)
            is_ativo = (i == self.algoritmo_idx)

            b_rect = self.desenhar_botao(alg, x_alg, y_alg, 300, 45, ativo=is_ativo, hover=is_hover)
            self.botoes_algoritmo.append((b_rect, i))

        # 2. Seleção de Cenário
        lbl_cen = self.fonte_subtitulo.render("2. Escolha o Cenário (Mapa):", True, COR_TEXTO)
        self.tela.blit(lbl_cen, (80, 310))

        for i, cen in enumerate(self.cenarios):
            x_cen = 80 + i * 215
            rect = pygame.Rect(x_cen, 350, 200, 45)
            is_hover = rect.collidepoint(pos_mouse)
            is_ativo = (i == self.cenario_idx)

            b_rect = self.desenhar_botao(cen, x_cen, 350, 200, 45, ativo=is_ativo, hover=is_hover)
            self.botoes_cenario.append((b_rect, i))

        # 3. Botão Iniciar
        rect_iniciar = pygame.Rect(self.largura // 2 - 120, 460, 240, 55)
        is_hover_iniciar = rect_iniciar.collidepoint(pos_mouse)

        pygame.draw.rect(self.tela, COR_HOVER if is_hover_iniciar else COR_PRIMARIA, rect_iniciar, border_radius=12)
        txt_iniciar = self.fonte_subtitulo.render("INICIAR MISSÃO", True, (255, 255, 255))
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
