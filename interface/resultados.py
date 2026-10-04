import sys
import pygame

# --- SEÇÃO 1: CONFIGURAÇÃO DE CORES E ESTILOS DA INTERFACE ---
COR_FUNDO = (245, 247, 250)
COR_CARD_JOGADOR = (238, 242, 255)  # Tom azulado claro para o humano
COR_CARD_AGENTE = (236, 253, 245)   # Tom verde claro para o agente
COR_TEXTO_ESCURO = (30, 41, 59)
COR_TEXTO_MUTED = (100, 116, 139)
COR_AZUL = (37, 99, 235)
COR_VERDE = (16, 185, 129)
COR_VERMELHO = (220, 38, 38)
COR_BORDA = (203, 213, 225)
COR_HOVER = (29, 78, 216)


class TelaResultados:
    """
    Classe responsável por renderizar a tela visual comparativa de resultados
    entre o Usuário (decisão humana) e o Agente Inteligente (algoritmo de busca).
    """

    def __init__(self, tela, dimensoes):
        # Armazena a referência da tela do Pygame e suas dimensões
        self.tela = tela
        self.largura, self.altura = dimensoes

        # --- SEÇÃO 2: INICIALIZAÇÃO DAS FONTES DOS MÓDULOS VISUAIS ---
        self.fonte_titulo = pygame.font.SysFont("Arial", 28, bold=True)
        self.fonte_subtitulo = pygame.font.SysFont("Arial", 20, bold=True)
        self.fonte_rotulo = pygame.font.SysFont("Arial", 16, bold=True)
        self.fonte_valor = pygame.font.SysFont("Arial", 16)
        self.fonte_destaque = pygame.font.SysFont("Arial", 18, bold=True)

    def desenhar_card_metricas(
        self, x, y, largura, altura, titulo, cor_fundo, metricas
    ):
        """
        Desenha um painel (card) com bordas arredondadas e exibe a lista de
        métricas no formato (Rótulo -> Valor).
        """
        # Desenho do retângulo de fundo do card
        rect_card = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(self.tela, cor_fundo, rect_card, border_radius=12)
        pygame.draw.rect(
            self.tela, COR_BORDA, rect_card, width=2, border_radius=12
        )

        # Desenho do título do participante
        surf_titulo = self.fonte_subtitulo.render(
            titulo, True, COR_TEXTO_ESCURO
        )
        self.tela.blit(surf_titulo, (x + 20, y + 20))

        # Iteração sobre a lista de métricas passadas para o card
        curr_y = y + 60
        for rotulo, valor in metricas:
            surf_rot = self.fonte_rotulo.render(rotulo, True, COR_TEXTO_ESCURO)
            surf_val = self.fonte_valor.render(
                str(valor), True, COR_TEXTO_MUTED
            )

            self.tela.blit(surf_rot, (x + 20, curr_y))
            self.tela.blit(
                surf_val, (x + largura - 20 - surf_val.get_width(), curr_y)
            )

            # Divisória sutil entre cada métrica
            pygame.draw.line(
                self.tela,
                COR_BORDA,
                (x + 20, curr_y + 25),
                (x + largura - 20, curr_y + 25),
                1,
            )
            curr_y += 33

    def desenhar_botao(self, texto, x, y, w, h, cor_padrao, pos_mouse):
        """
        Desenha um botão interativo com destaque ao passar o mouse (hover)
        e retorna o seu retângulo de colisão.
        """
        rect = pygame.Rect(x, y, w, h)
        is_hover = rect.collidepoint(pos_mouse)
        cor_final = COR_HOVER if is_hover else cor_padrao

        pygame.draw.rect(self.tela, cor_final, rect, border_radius=8)
        pygame.draw.rect(self.tela, COR_BORDA, rect, width=1, border_radius=8)

        surf_txt = self.fonte_subtitulo.render(texto, True, (255, 255, 255))
        self.tela.blit(surf_txt, surf_txt.get_rect(center=rect.center))
        return rect

    def exibir(self, estado_jogador, estado_agente, nome_algoritmo, nome_cenario):
        """
        Loop principal de exibição da tela de resultados.
        Retorna a opção escolhida pelo jogador: 'REINICIAR', 'MENU' ou 'SAIR'.
        """
        relogio = pygame.time.Clock()

        # --- SEÇÃO 3: FORMATAÇÃO E PREPARAÇÃO DOS DADOS ---
        # Resumo do caminho percorrido/encontrado
        cam_humano_str = f"{len(estado_jogador.caminho)} posições"
        cam_agente_str = f"{len(estado_agente.caminho_pre_calculado)} posições"

        # Montagem dos dados do Usuário
        metricas_jogador = [
            ("Tempo Necessário:", f"{estado_jogador.tempo:.2f} s"),
            ("Quantidade de Passos:", f"{estado_jogador.passos}"),
            ("Custo Total do Caminho:", f"{estado_jogador.custo}"),
            ("Caminho Encontrado:", cam_humano_str),
        ]

        # Montagem dos dados do Agente com todas as métricas exigidas
        metricas_agente = [
            (
                "Tempo de Execução (Busca):",
                f"{estado_agente.tempo_execucao * 1000:.3f} ms",
            ),
            ("Quantidade de Passos:", f"{estado_agente.passos}"),
            ("Custo Total do Caminho:", f"{estado_agente.custo}"),
            ("Estados Expandidos:", f"{estado_agente.estados_expandidos}"),
            ("Estados Gerados:", f"{estado_agente.estados_gerados}"),
            (
                "Tamanho Máx. da Fronteira:",
                f"{estado_agente.fronteira_max}",
            ),
            ("Caminho Encontrado:", cam_agente_str),
        ]

        # Lógica de determinação de eficiência de custo entre humano x agente
        if estado_jogador.custo < estado_agente.custo:
            vencedor_str = "Usuário obteve menor custo de caminho!"
        elif estado_agente.custo < estado_jogador.custo:
            vencedor_str = f"Agente ({nome_algoritmo}) obteve menor custo!"
        else:
            vencedor_str = (
                "Empate! Ambos encontraram o mesmo custo de caminho."
            )

        # --- SEÇÃO 4: LOOP DE RENDERIZAÇÃO E INTERAÇÃO ---
        while True:
            pos_mouse = pygame.mouse.get_pos()
            self.tela.fill(COR_FUNDO)

            # Título superior
            txt_titulo = self.fonte_titulo.render(
                "Resultados Comparativos da Missão", True, COR_TEXTO_ESCURO
            )
            txt_sub = self.fonte_valor.render(
                f"Algoritmo: {nome_algoritmo} | Cenário: {nome_cenario}",
                True,
                COR_TEXTO_MUTED,
            )
            self.tela.blit(
                txt_titulo,
                (self.largura // 2 - txt_titulo.get_width() // 2, 25),
            )
            self.tela.blit(
                txt_sub, (self.largura // 2 - txt_sub.get_width() // 2, 65)
            )

            # Banner indicativo de comparação
            rect_banner = pygame.Rect(self.largura // 2 - 320, 100, 640, 45)
            pygame.draw.rect(
                self.tela, COR_CARD_AGENTE, rect_banner, border_radius=8
            )
            pygame.draw.rect(
                self.tela, COR_VERDE, rect_banner, width=2, border_radius=8
            )
            txt_venc = self.fonte_destaque.render(
                vencedor_str, True, COR_TEXTO_ESCURO
            )
            self.tela.blit(
                txt_venc, txt_venc.get_rect(center=rect_banner.center)
            )

            # Renderização dos Cards comparativos
            largura_card = 580
            altura_card = 350
            y_cards = 165

            self.desenhar_card_metricas(
                int(self.largura * 0.25 - largura_card // 2),
                y_cards,
                largura_card,
                altura_card,
                "Usuário (Decisão Humana)",
                COR_CARD_JOGADOR,
                metricas_jogador,
            )

            self.desenhar_card_metricas(
                int(self.largura * 0.75 - largura_card // 2),
                y_cards,
                largura_card,
                altura_card,
                f"Agente ({nome_algoritmo})",
                COR_CARD_AGENTE,
                metricas_agente,
            )

            # Desenho dos botões de ação no rodapé
            y_botoes = 560
            btn_reiniciar = self.desenhar_botao(
                "Reiniciar Missão",
                self.largura // 2 - 320,
                y_botoes,
                200,
                50,
                COR_AZUL,
                pos_mouse,
            )
            btn_menu = self.desenhar_botao(
                "Menu Principal",
                self.largura // 2 - 100,
                y_botoes,
                200,
                50,
                COR_VERDE,
                pos_mouse,
            )
            btn_sair = self.desenhar_botao(
                "Sair",
                self.largura // 2 + 120,
                y_botoes,
                200,
                50,
                COR_VERMELHO,
                pos_mouse,
            )

            # Trata ações de clique
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if btn_reiniciar.collidepoint(event.pos):
                        return "REINICIAR"
                    elif btn_menu.collidepoint(event.pos):
                        return "MENU"
                    elif btn_sair.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            relogio.tick(30)