from functools import lru_cache

import pygame

from ambiente.celula import (
    DIFICIL,
    FOCO,
    GRAMA,
    IMAGEM_FOCO,
    LIVRE,
    MENSAGEM_FOCO,
    OBSTACULO,
)

# --- DEFINIÇÃO DE CORES ---
BRANCO = (255, 255, 255)
COR_FUNDO = (241, 245, 249)
COR_BORDA = (226, 232, 240)
COR_SOMBRA = (215, 222, 232)
COR_TEXTO = (15, 23, 42)
COR_TEXTO_MUTED = (100, 116, 139)
COR_PRIMARIA = (37, 99, 235)
COR_VERDE = (16, 185, 129)
COR_AMBAR = (217, 119, 6)
COR_VERMELHO = (220, 38, 38)
COR_CAIXA_METRICA = (248, 250, 252)
COR_GRADE = (203, 213, 225)

# Cores correspondentes aos tipos de terreno na matriz
COR_LIVRE = (236, 239, 243)      # Tipo 0
COR_GRAMA = (163, 230, 163)      # Tipo 1
COR_DIFICIL = (160, 110, 70)     # Tipo 2
COR_OBSTACULO = (71, 85, 105)    # Tipo 3

# Cores da visualização da busca do agente
COR_EXPLORADO = (253, 224, 71)   # Posições expandidas pela busca (amarelo)
COR_CAMINHO = (239, 68, 68)      # Caminho efetivamente percorrido (vermelho)

# --- MEDIDAS DO LAYOUT DA TELA PRINCIPAL ---
ALTURA_CABECALHO = 76
ALTURA_LEGENDA = 44
ESPACO_ENTRE_CARDS = 48
PADDING_CARD = 24
ALTURA_TITULO_CARD = 60
ALTURA_METRICAS_CARD = 96
LARGURA_MIN_CONTEUDO_CARD = 480
TAMANHO_MAX_CELULA = 56


@lru_cache(maxsize=None)
def fonte(tamanho, negrito=False, italico=False):
    """Retorna (e reaproveita) a fonte padrão da interface."""
    if not pygame.font.get_init():
        pygame.font.init()
    return pygame.font.SysFont("segoeui,arial", tamanho, bold=negrito, italic=italico)


def desenhar_texto(tela, texto, x, y, tamanho=18, cor=COR_TEXTO, negrito=False, centralizado=False):
    superficie = fonte(tamanho, negrito).render(texto, True, cor)
    retangulo = superficie.get_rect()
    if centralizado:
        retangulo.center = (x, y)
    else:
        retangulo.topleft = (x, y)
    tela.blit(superficie, retangulo)
    return retangulo


def quebrar_texto(texto, fonte_texto, largura_max):
    """Divide o texto em linhas que caibam em 'largura_max' pixels."""
    linhas = []
    linha_atual = ""
    for palavra in texto.split():
        tentativa = f"{linha_atual} {palavra}".strip()
        if fonte_texto.size(tentativa)[0] <= largura_max:
            linha_atual = tentativa
        else:
            linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)
    return linhas


def desenhar_card(tela, retangulo, cor=BRANCO, raio=16):
    """Painel com cantos arredondados, sombra suave e borda."""
    sombra = retangulo.move(0, 4)
    pygame.draw.rect(tela, COR_SOMBRA, sombra, border_radius=raio)
    pygame.draw.rect(tela, cor, retangulo, border_radius=raio)
    pygame.draw.rect(tela, COR_BORDA, retangulo, width=1, border_radius=raio)


def desenhar_selo(tela, texto, cor, x_direita, centro_y):
    """Desenha um selo (pill) de status alinhado à direita em 'x_direita'."""
    surf = fonte(14, True).render(texto, True, BRANCO)
    rect = pygame.Rect(0, 0, surf.get_width() + 24, 28)
    rect.midright = (x_direita, centro_y)
    pygame.draw.rect(tela, cor, rect, border_radius=14)
    tela.blit(surf, surf.get_rect(center=rect.center))


def desenhar_botao_voltar(tela, x=24, y=20):
    rect = pygame.Rect(x, y, 110, 36)
    hover = rect.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(tela, COR_BORDA if hover else COR_FUNDO, rect, border_radius=10)
    pygame.draw.rect(tela, COR_GRADE, rect, width=1, border_radius=10)

    # Seta desenhada manualmente para não depender da fonte
    cx, cy = rect.x + 24, rect.centery
    pygame.draw.polygon(tela, COR_TEXTO, [(cx - 6, cy), (cx + 2, cy - 7), (cx + 2, cy + 7)])
    pygame.draw.line(tela, COR_TEXTO, (cx, cy), (cx + 10, cy), 3)

    desenhar_texto(tela, "Menu", rect.x + 44, rect.y + 7, tamanho=17, negrito=True)
    return rect


def definir_cor_por_terreno(valor_celula):
    if valor_celula == LIVRE:
        return COR_LIVRE
    elif valor_celula == GRAMA:
        return COR_GRAMA
    elif valor_celula == DIFICIL:
        return COR_DIFICIL
    elif valor_celula == OBSTACULO:
        return COR_OBSTACULO
    return COR_LIVRE


def calcular_tamanho_celula(cenario, dimensoes_tela):
    """
    Calcula o tamanho de cada célula para que os dois mapas caibam lado a
    lado na tela, aproveitando o espaço disponível.
    """
    largura_tela, altura_tela = dimensoes_tela

    largura_disponivel = (largura_tela - ESPACO_ENTRE_CARDS) / 2 - 2 * PADDING_CARD - 40
    altura_disponivel = (
        altura_tela - ALTURA_CABECALHO - ALTURA_LEGENDA
        - ALTURA_TITULO_CARD - ALTURA_METRICAS_CARD - 2 * PADDING_CARD - 48
    )

    tamanho = min(largura_disponivel / cenario.colunas, altura_disponivel / cenario.linhas)
    return int(min(tamanho, TAMANHO_MAX_CELULA))


def desenhar_mapa(tela, cenario, offset_x, offset_y, tamanho_celula, pos_personagem, dicionario_imagens,
                  celulas_exploradas=(), celulas_caminho=()):
    """
    Renderiza a grade utilizando o objeto Cenario completo.
    dicionario_imagens deve conter as superfícies do pygame carregadas usando
    os nomes de arquivo como chave (ex: imagens["rocha.png"]).
    celulas_exploradas são pintadas de amarelo e celulas_caminho de vermelho.
    """
    exploradas = set(celulas_exploradas)
    caminho = set(celulas_caminho)

    for linha in range(cenario.linhas):
        for coluna in range(cenario.colunas):
            x = offset_x + (coluna * tamanho_celula)
            y = offset_y + (linha * tamanho_celula)
            rect_celula = pygame.Rect(x, y, tamanho_celula, tamanho_celula)
            valor_celula = cenario.mapa[linha][coluna]
            posicao_atual = (linha, coluna)

            # 1. Fundo do terreno (ou cor da busca do agente)
            if posicao_atual in caminho:
                cor = COR_CAMINHO
            elif posicao_atual in exploradas:
                cor = COR_EXPLORADO
            else:
                cor = definir_cor_por_terreno(valor_celula)
            pygame.draw.rect(tela, cor, rect_celula)

            # 2. Contorno da grade
            pygame.draw.rect(tela, COR_GRADE, rect_celula, 1)

            # 3. Decorações de Obstáculos
            if valor_celula == OBSTACULO and posicao_atual in cenario.decoracoes:
                nome_imagem = cenario.decoracoes[posicao_atual]
                if nome_imagem in dicionario_imagens:
                    tela.blit(dicionario_imagens[nome_imagem], (x, y))

            # 4. Desenha os Focos (o foco objetivo recebe um contorno de destaque)
            if valor_celula == FOCO and posicao_atual in cenario.focos:
                nome_img_foco = IMAGEM_FOCO.get(cenario.focos[posicao_atual])
                if nome_img_foco in dicionario_imagens:
                    tela.blit(dicionario_imagens[nome_img_foco], (x, y))
                if posicao_atual == cenario.objetivo:
                    pygame.draw.rect(tela, COR_TEXTO, rect_celula, 3)

            # 5. Personagem (Jogador ou Agente)
            if posicao_atual == pos_personagem and "personagem" in dicionario_imagens:
                tela.blit(dicionario_imagens["personagem"], (x, y))

    rect_mapa = pygame.Rect(offset_x, offset_y, cenario.colunas * tamanho_celula, cenario.linhas * tamanho_celula)
    pygame.draw.rect(tela, COR_GRADE, rect_mapa.inflate(4, 4), width=2, border_radius=4)


def desenhar_metricas(tela, x, y, largura, metricas):
    """Desenha uma fileira de caixas (rótulo em cima, valor em destaque)."""
    espaco = 12
    largura_caixa = (largura - espaco * (len(metricas) - 1)) / len(metricas)
    for i, (rotulo, valor) in enumerate(metricas):
        rect = pygame.Rect(int(x + i * (largura_caixa + espaco)), y, int(largura_caixa), 72)
        pygame.draw.rect(tela, COR_CAIXA_METRICA, rect, border_radius=10)
        pygame.draw.rect(tela, COR_BORDA, rect, width=1, border_radius=10)
        desenhar_texto(tela, rotulo, rect.centerx, rect.y + 20, tamanho=14, cor=COR_TEXTO_MUTED, centralizado=True)
        desenhar_texto(tela, valor, rect.centerx, rect.y + 48, tamanho=22, negrito=True, centralizado=True)


def desenhar_painel_participante(tela, rect_card, titulo, subtitulo, status, cenario, tamanho_celula,
                                 estado, imagens, metricas, celulas_exploradas=(), celulas_caminho=()):
    desenhar_card(tela, rect_card)

    x_conteudo = rect_card.x + PADDING_CARD
    largura_conteudo = rect_card.width - 2 * PADDING_CARD

    # Título, subtítulo e selo de status
    desenhar_texto(tela, titulo, x_conteudo, rect_card.y + 18, tamanho=22, negrito=True)
    desenhar_texto(tela, subtitulo, x_conteudo, rect_card.y + 46, tamanho=14, cor=COR_TEXTO_MUTED)
    texto_status, cor_status = status
    desenhar_selo(tela, texto_status, cor_status, rect_card.right - PADDING_CARD, rect_card.y + 36)

    # Mapa centralizado dentro do card
    largura_mapa = cenario.colunas * tamanho_celula
    altura_mapa = cenario.linhas * tamanho_celula
    x_mapa = rect_card.centerx - largura_mapa // 2
    y_mapa = rect_card.y + ALTURA_TITULO_CARD + PADDING_CARD
    desenhar_mapa(tela, cenario, x_mapa, y_mapa, tamanho_celula, estado.posicao, imagens,
                  celulas_exploradas, celulas_caminho)

    desenhar_metricas(tela, x_conteudo, y_mapa + altura_mapa + PADDING_CARD, largura_conteudo, metricas)


def desenhar_legenda(tela, centro_x, y, cenario):
    itens = [
        (COR_LIVRE, f"Livre ({cenario.custos.get(LIVRE, '-')})"),
        (COR_GRAMA, f"Grama ({cenario.custos.get(GRAMA, '-')})"),
        (COR_DIFICIL, f"Difícil ({cenario.custos.get(DIFICIL, '-')})"),
        (COR_OBSTACULO, "Obstáculo"),
        (COR_EXPLORADO, "Explorado pelo agente"),
        (COR_CAMINHO, "Caminho do agente"),
    ]
    fonte_legenda = fonte(15)
    lado, espaco_interno, espaco_itens = 18, 8, 28

    larguras = [lado + espaco_interno + fonte_legenda.size(texto)[0] for _, texto in itens]
    x = centro_x - (sum(larguras) + espaco_itens * (len(itens) - 1)) // 2

    for (cor, texto), largura in zip(itens, larguras):
        quadrado = pygame.Rect(x, y, lado, lado)
        pygame.draw.rect(tela, cor, quadrado, border_radius=4)
        pygame.draw.rect(tela, COR_GRADE, quadrado, width=1, border_radius=4)
        desenhar_texto(tela, texto, x + lado + espaco_interno, y, tamanho=15, cor=COR_TEXTO_MUTED)
        x += largura + espaco_itens


def desenhar_tela_principal(tela, dimensoes_tela, cenario, estado_jogador, estado_agente, imagens_jogador,
                            imagens_agente, tamanho_celula=40, nome_algoritmo=""):
    largura_tela, altura_tela = dimensoes_tela
    tela.fill(COR_FUNDO)

    # --- Cabeçalho ---
    pygame.draw.rect(tela, BRANCO, (0, 0, largura_tela, ALTURA_CABECALHO))
    pygame.draw.line(tela, COR_BORDA, (0, ALTURA_CABECALHO - 1), (largura_tela, ALTURA_CABECALHO - 1))
    rect_voltar = desenhar_botao_voltar(tela)
    desenhar_texto(tela, "Combate à Dengue", largura_tela // 2, 28, tamanho=26, negrito=True, centralizado=True)
    subtitulo = f"{nome_algoritmo}  •  {cenario.nome}" if nome_algoritmo else cenario.nome
    desenhar_texto(tela, subtitulo, largura_tela // 2, 56, tamanho=15, cor=COR_TEXTO_MUTED, centralizado=True)

    # --- Dimensões dos cards, centralizados na área abaixo do cabeçalho ---
    largura_mapa = cenario.colunas * tamanho_celula
    altura_mapa = cenario.linhas * tamanho_celula
    largura_card = max(largura_mapa, LARGURA_MIN_CONTEUDO_CARD) + 2 * PADDING_CARD
    altura_card = ALTURA_TITULO_CARD + PADDING_CARD + altura_mapa + PADDING_CARD + ALTURA_METRICAS_CARD

    altura_conteudo = altura_card + 24 + ALTURA_LEGENDA
    y_card = ALTURA_CABECALHO + (altura_tela - ALTURA_CABECALHO - altura_conteudo) // 2
    x_card_jogador = largura_tela // 2 - ESPACO_ENTRE_CARDS // 2 - largura_card
    x_card_agente = largura_tela // 2 + ESPACO_ENTRE_CARDS // 2

    # --- Card do Jogador ---
    if estado_jogador.concluiu:
        status_jogador = ("Concluído", COR_VERDE)
    else:
        status_jogador = ("Em jogo", COR_PRIMARIA)

    desenhar_painel_participante(
        tela, pygame.Rect(x_card_jogador, y_card, largura_card, altura_card),
        "Jogador", "Use as setas do teclado para chegar ao foco", status_jogador,
        cenario, tamanho_celula, estado_jogador, imagens_jogador,
        [
            ("Tempo", f"{estado_jogador.tempo:.2f} s"),
            ("Passos", f"{estado_jogador.passos}"),
            ("Custo", f"{estado_jogador.custo}"),
        ],
    )

    # --- Card do Agente ---
    explorando = estado_agente.indice_exploracao < len(estado_agente.explorados)
    if estado_agente.concluiu:
        status_agente = ("Concluído", COR_VERDE)
    elif explorando:
        status_agente = ("Explorando", COR_AMBAR)
    else:
        status_agente = ("Percorrendo", COR_PRIMARIA)

    desenhar_painel_participante(
        tela, pygame.Rect(x_card_agente, y_card, largura_card, altura_card),
        "Agente", f"Busca: {nome_algoritmo}" if nome_algoritmo else "Agente inteligente", status_agente,
        cenario, tamanho_celula, estado_agente, imagens_agente,
        [
            ("Busca", f"{estado_agente.tempo_execucao * 1000:.3f} ms"),
            ("Explorados", f"{estado_agente.indice_exploracao}"),
            ("Passos", f"{estado_agente.passos}"),
            ("Custo", f"{estado_agente.custo}"),
        ],
        celulas_exploradas=estado_agente.explorados[:estado_agente.indice_exploracao],
        celulas_caminho=[] if explorando else estado_agente.caminho,
    )

    # --- Legenda ---
    desenhar_legenda(tela, largura_tela // 2, y_card + altura_card + 24 + 12, cenario)

    return rect_voltar


def mostrar_mensagem_educativa(tela, resolucao, tipo_foco):
    largura, altura = resolucao

    # Escurece a tela ao fundo para destacar a mensagem
    veu = pygame.Surface((largura, altura), pygame.SRCALPHA)
    veu.fill((15, 23, 42, 140))
    tela.blit(veu, (0, 0))

    # Título e orientação definidos em ambiente.celula para cada tipo de foco
    if tipo_foco in MENSAGEM_FOCO:
        titulo_txt, *partes_desc = MENSAGEM_FOCO[tipo_foco]
        desc_txt = " ".join(parte.strip() for parte in partes_desc)
    else:
        titulo_txt = f"{str(tipo_foco).capitalize()} com água acumulada!"
        desc_txt = "Elimine a água parada deste recipiente para evitar a proliferação do mosquito da dengue."

    largura_painel = 720
    fonte_desc = fonte(18)
    linhas_desc = quebrar_texto(desc_txt, fonte_desc, largura_painel - 80)
    altura_painel = 150 + len(linhas_desc) * 26

    rect_painel = pygame.Rect(0, 0, largura_painel, altura_painel)
    rect_painel.center = (largura // 2, altura // 2)
    pygame.draw.rect(tela, BRANCO, rect_painel, border_radius=18)
    pygame.draw.rect(tela, COR_VERMELHO, (rect_painel.x, rect_painel.y, largura_painel, 8),
                     border_top_left_radius=18, border_top_right_radius=18)

    y = rect_painel.y + 36
    desenhar_texto(tela, "MISSÃO CONCLUÍDA", rect_painel.centerx, y, tamanho=14, negrito=True,
                   cor=COR_TEXTO_MUTED, centralizado=True)
    y += 32
    desenhar_texto(tela, titulo_txt, rect_painel.centerx, y, tamanho=24, negrito=True,
                   cor=COR_VERMELHO, centralizado=True)
    y += 40
    for linha in linhas_desc:
        desenhar_texto(tela, linha, rect_painel.centerx, y, tamanho=18, centralizado=True)
        y += 26

    y += 16
    desenhar_texto(tela, "Pressione [ENTER] para ver os resultados finais", rect_painel.centerx, y,
                   tamanho=15, cor=COR_TEXTO_MUTED, centralizado=True)

    # ATENÇÃO: Nenhum pygame.display.flip() ou while loop aqui!
    # A função apenas desenha no buffer e retorna.
