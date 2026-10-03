import sys

import pygame

from ambiente.celula import DIFICIL, FOCO, GRAMA, LIVRE, MENSAGEM_FOCO, OBSTACULO

# --- DEFINIÇÃO DE CORES ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
CINZA_ESCURO = (100, 100, 100)
VERMELHO = (255, 0, 0)

# Cores correspondentes aos tipos de terreno na matriz
COR_LIVRE = (230, 230, 230)      # Tipo 0
COR_GRAMA = (144, 238, 144)      # Tipo 1
COR_DIFICIL = (139, 69, 19)      # Tipo 2
COR_OBSTACULO = (50, 50, 50)     # Tipo 3

def inicializar_fonte(tamanho=24):
    if not pygame.font.get_init():
        pygame.font.init()
    return pygame.font.SysFont(None, tamanho)

def desenhar_texto(tela, texto, x, y, tamanho=24, cor=PRETO, centralizado=False):
    fonte = inicializar_fonte(tamanho)
    superficie = fonte.render(texto, True, cor)
    retangulo = superficie.get_rect()
    if centralizado:
        retangulo.center = (x, y)
    else:
        retangulo.topleft = (x, y)
    tela.blit(superficie, retangulo)

def desenhar_botao_voltar(tela, x=20, y=20):
    pygame.draw.circle(tela, CINZA_ESCURO, (x + 15, y + 15), 20)
    desenhar_texto(tela, "<-", x + 5, y + 5, tamanho=30, cor=BRANCO)
    return pygame.Rect(x - 5, y - 5, 40, 40)

def definir_cor_por_terreno(valor_celula):
    if valor_celula == LIVRE:
        return COR_LIVRE
    elif valor_celula == GRAMA:
        return COR_GRAMA
    elif valor_celula == DIFICIL:
        return COR_DIFICIL
    elif valor_celula == OBSTACULO:
        return COR_OBSTACULO
    return BRANCO

def desenhar_mapa(tela, cenario, offset_x, offset_y, tamanho_celula, pos_personagem, dicionario_imagens):
    """
    Renderiza a grade utilizando o objeto Cenario completo.
    dicionario_imagens deve conter as superfícies do pygame carregadas usando
    os nomes de arquivo como chave (ex: imagens["rocha.png"]).
    """
    for linha in range(cenario.linhas):
        for coluna in range(cenario.colunas):
            x = offset_x + (coluna * tamanho_celula)
            y = offset_y + (linha * tamanho_celula)
            valor_celula = cenario.mapa[linha][coluna]

            # 1. Fundo do terreno
            cor_terreno = definir_cor_por_terreno(valor_celula)
            pygame.draw.rect(tela, cor_terreno, (x, y, tamanho_celula, tamanho_celula))

            # 2. Contorno da grade
            pygame.draw.rect(tela, CINZA, (x, y, tamanho_celula, tamanho_celula), 1)

            posicao_atual = (linha, coluna)

            # 3. Decorações de Obstáculos
            if valor_celula == OBSTACULO and posicao_atual in cenario.decoracoes:
                nome_imagem = cenario.decoracoes[posicao_atual]
                if nome_imagem in dicionario_imagens:
                    tela.blit(dicionario_imagens[nome_imagem], (x, y))

            # 4. Desenha os Focos
            if valor_celula == FOCO and posicao_atual in cenario.focos:
                tipo_foco = cenario.focos[posicao_atual]
                # Precisaria de um mapeamento de tipo_foco para nome do arquivo na main.py
                nome_img_foco = f"{tipo_foco}.png"
                if nome_img_foco in dicionario_imagens:
                    tela.blit(dicionario_imagens[nome_img_foco], (x, y))

            # 5. Personagem (Jogador ou Agente)
            if posicao_atual == pos_personagem and "personagem" in dicionario_imagens:
                tela.blit(dicionario_imagens["personagem"], (x, y))

def desenhar_tela_principal(tela, dimensoes_tela, cenario, estado_jogador, estado_agente, imagens_jogador, imagens_agente, tamanho_celula=40):
    largura_tela, _altura_tela = dimensoes_tela
    tela.fill(BRANCO)

    rect_voltar = desenhar_botao_voltar(tela)

    centro_jogador = largura_tela * 0.25
    centro_agente = largura_tela * 0.75

    desenhar_texto(tela, "JOGADOR", centro_jogador, 50, tamanho=36, centralizado=True)
    desenhar_texto(tela, "AGENTE", centro_agente, 50, tamanho=36, centralizado=True)

    largura_mapa = cenario.colunas * tamanho_celula
    offset_x_jogador = centro_jogador - (largura_mapa / 2)
    offset_x_agente = centro_agente - (largura_mapa / 2)
    offset_y_mapas = 100

    desenhar_mapa(tela, cenario, offset_x_jogador, offset_y_mapas, tamanho_celula, estado_jogador.posicao, imagens_jogador)
    desenhar_mapa(tela, cenario, offset_x_agente, offset_y_mapas, tamanho_celula, estado_agente.posicao, imagens_agente)

    altura_mapa = cenario.linhas * tamanho_celula
    y_metricas = offset_y_mapas + altura_mapa + 30

    desenhar_texto(tela, f"Tempo: {estado_jogador.tempo:.2f}s", offset_x_jogador, y_metricas)
    desenhar_texto(tela, f"Passos: {estado_jogador.passos}", offset_x_jogador, y_metricas + 30)
    desenhar_texto(tela, f"Custo: {estado_jogador.custo}", offset_x_jogador, y_metricas + 60)

    desenhar_texto(tela, f"Tempo: {estado_agente.tempo_execucao:.5f}s", offset_x_agente, y_metricas)
    desenhar_texto(tela, f"Passos: {estado_agente.passos}", offset_x_agente, y_metricas + 30)
    desenhar_texto(tela, f"Custo: {estado_agente.custo}", offset_x_agente, y_metricas + 60)

    pygame.display.flip()
    return rect_voltar

def mostrar_mensagem_educativa(tela, resolucao, tipo_foco):
    largura, altura = resolucao
    altura_painel = 120

    rect_msg = pygame.Rect(0, altura - altura_painel, largura, altura_painel)

    pygame.draw.rect(tela, (245, 247, 250), rect_msg)
    pygame.draw.rect(tela, (220, 38, 38), rect_msg, width=4)

    fonte_titulo = pygame.font.SysFont("Arial", 22, bold=True)
    fonte_texto = pygame.font.SysFont("Arial", 18)
    fonte_dica = pygame.font.SysFont("Arial", 14, italic=True)

    titulo_txt = f"{str(tipo_foco).upper()} COM ÁGUA ACUMULADA!"

    if "pneu" in str(tipo_foco).lower():
        desc_txt = "Pneus expostos podem acumular água e se tornar criadouros. Fure, cubra ou armazene-os em local protegido."
    else:
        desc_txt = "Elimine a água parada deste recipiente para evitar a proliferação do mosquito da dengue."

    dica_txt = "Pressione [ENTER] para ver os resultados finais"

    surf_titulo = fonte_titulo.render(titulo_txt, True, (220, 38, 38))
    surf_desc = fonte_texto.render(desc_txt, True, (30, 41, 59))
    surf_dica = fonte_dica.render(dica_txt, True, (100, 116, 139))

    tela.blit(surf_titulo, (largura // 2 - surf_titulo.get_width() // 2, altura - altura_painel + 15))
    tela.blit(surf_desc, (largura // 2 - surf_desc.get_width() // 2, altura - altura_painel + 50))
    tela.blit(surf_dica, (largura // 2 - surf_dica.get_width() // 2, altura - altura_painel + 90))

    # ATENÇÃO: Nenhum pygame.display.flip() ou while loop aqui!
    # A função apenas desenha no buffer e retorna.
