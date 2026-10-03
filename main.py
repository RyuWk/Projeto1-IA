import os
import sys
import time

import pygame

from algoritmos.a_estrela import busca_a_estrela
from algoritmos.bfs import bfs
from algoritmos.dfs import dfs
from algoritmos.gulosa import busca_gulosa
from ambiente.celula import (
    IMAGEM_AGENTE,
    IMAGEM_FOCO,
    IMAGEM_OBSTACULO,
    IMAGEM_USUARIO,
    OBSTACULO,
)

# Importações dos módulos do projeto[cite: 15]
from ambiente.cenarios_padrao import obter_cenario
from interface.interface import desenhar_tela_principal, mostrar_mensagem_educativa
from interface.menu import (
    MenuInicial,  # Integração da classe exata fornecida[cite: 14, 15]
)


class EstadoParticipante:
    """Classe auxiliar para armazenar as métricas em tempo real de cada participante."""
    def __init__(self, inicio):
        self.posicao = inicio
        self.passos = 0
        self.custo = 0
        self.tempo = 0.0
        self.tempo_execucao = 0.0
        self.concluiu = False
        self.caminho = [inicio]

        self.indice_caminho = 0
        self.caminho_pre_calculado = []

def carregar_imagens(tamanho_celula=40):
    imagens = {}
    caminho_base = os.path.join("ambiente", "imagens")

    def carregar(nome_arquivo):
        caminho_completo = os.path.join(caminho_base, nome_arquivo)
        try:
            img = pygame.image.load(caminho_completo).convert_alpha()
            return pygame.transform.scale(img, (tamanho_celula, tamanho_celula))
        except FileNotFoundError:
            surf = pygame.Surface((tamanho_celula, tamanho_celula))
            surf.fill((255, 0, 255))
            return surf

    for arquivo in IMAGEM_FOCO.values():
        imagens[arquivo] = carregar(arquivo)

    for arquivo in IMAGEM_OBSTACULO.values():
        imagens[arquivo] = carregar(arquivo)

    imagens["usuario"] = carregar(IMAGEM_USUARIO)
    imagens["agente"] = carregar(IMAGEM_AGENTE)

    return imagens

def processar_movimento_jogador(evento_tecla, estado, cenario):
    if estado.concluiu:
        return

    linha, coluna = estado.posicao
    nova_posicao = estado.posicao

    if evento_tecla == pygame.K_UP:
        nova_posicao = (linha - 1, coluna)
    elif evento_tecla == pygame.K_DOWN:
        nova_posicao = (linha + 1, coluna)
    elif evento_tecla == pygame.K_LEFT:
        nova_posicao = (linha, coluna - 1)
    elif evento_tecla == pygame.K_RIGHT:
        nova_posicao = (linha, coluna + 1)

    if cenario._dentro_dos_limites(nova_posicao):  # noqa: SIM102
        if cenario.mapa[nova_posicao[0]][nova_posicao[1]] != OBSTACULO:
            estado.posicao = nova_posicao
            estado.passos += 1
            estado.custo += cenario.obter_custo(nova_posicao)
            estado.caminho.append(nova_posicao)

            if cenario.teste_objetivo(nova_posicao):
                estado.concluiu = True


def main():
    pygame.init()

    LARGURA, ALTURA = 1600, 900

    # 1. INTEGRAÇÃO DO MENU[cite: 14]
    # Instancia o menu e assume o controle da tela até o clique no botão Iniciar[cite: 14]
    menu = MenuInicial(LARGURA, ALTURA)
    escolhas_usuario = menu.executar()

    # Extração das opções configuradas pelo usuário[cite: 14]
    nome_algoritmo = escolhas_usuario["algoritmo"]
    # Ajuste do índice (0, 1, 2) para o ID real do cenário (1, 2, 3)
    id_cenario = escolhas_usuario["cenario_idx"] + 1

    # Retoma o controle da tela para a simulação principal
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(f"Combate à Dengue - IA ({nome_algoritmo} | Cenário {id_cenario})")
    relogio = pygame.time.Clock()

    todas_imagens = carregar_imagens(tamanho_celula=40)

    imagens_jogador = todas_imagens.copy()
    imagens_jogador["personagem"] = todas_imagens["usuario"]
    imagens_agente = todas_imagens.copy()
    imagens_agente["personagem"] = todas_imagens["agente"]

    rodando_app = True
    while rodando_app:

        # Carrega o cenário escolhido no menu
        cenario = obter_cenario(id_cenario)

        # ----------------- INTEGRAÇÃO DOS ALGORITMOS -----------------
            # Verifica a string vinda do menu para acionar a função correta
        if "BFS" in nome_algoritmo:
            resultado_agente = bfs(cenario)
        elif "DFS" in nome_algoritmo:
            resultado_agente = dfs(cenario)
        elif "Gulosa" in nome_algoritmo:
            resultado_agente = busca_gulosa(cenario)
        elif "A*" in nome_algoritmo:
            resultado_agente = busca_a_estrela(cenario)
        else:
            resultado_agente = bfs(cenario) # Fallback de segurança
        # ------------------- FIM MOCK --------------------------------

        # 2. Inicializar estados considerando que o usuário e agente devem resolver a mesma instância[cite: 18]
        estado_jogador = EstadoParticipante(cenario.inicio)
        estado_agente = EstadoParticipante(cenario.inicio)

        estado_agente.caminho_pre_calculado = resultado_agente["caminho"]
        estado_agente.tempo_execucao = resultado_agente["tempo_execucao"]

        # 3. Variáveis de Controle da Simulação
        TEMPO_MOVIMENTO_AGENTE = 500
        ultimo_tempo_agente = pygame.time.get_ticks()
        tempo_inicio_missao = time.time()

        missao_ativa = True
        mostrar_resultados_finais = False

        # 4. LOOP DA MISSÃO SIMULTÂNEA[cite: 18]
        while missao_ativa:
            tempo_atual = pygame.time.get_ticks()

            # A. Processamento de Eventos (Usuário)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    missao_ativa = False
                    rodando_app = False

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if retangulo_voltar.collidepoint(evento.pos):
                        # Quebra o loop da missão e permite voltar (você pode redirecionar pro menu aqui)
                        main()
                        return

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and estado_jogador.concluiu and estado_agente.concluiu:
                        mostrar_resultados_finais = True
                        missao_ativa = False

                    elif not estado_jogador.concluiu:
                        processar_movimento_jogador(evento.key, estado_jogador, cenario)
                        if estado_jogador.concluiu:
                            estado_jogador.tempo = time.time() - tempo_inicio_missao

            # B. Movimentação Automática do Agente
            if not estado_agente.concluiu:  # noqa: SIM102
                if tempo_atual - ultimo_tempo_agente > TEMPO_MOVIMENTO_AGENTE:
                    if estado_agente.indice_caminho < len(estado_agente.caminho_pre_calculado) - 1:
                        estado_agente.indice_caminho += 1
                        nova_pos = estado_agente.caminho_pre_calculado[estado_agente.indice_caminho]

                        estado_agente.posicao = nova_pos
                        estado_agente.passos += 1
                        estado_agente.custo += cenario.obter_custo(nova_pos)

                        if cenario.teste_objetivo(nova_pos):
                            estado_agente.concluiu = True

                    ultimo_tempo_agente = tempo_atual

            # C. Atualização do Cronômetro do Jogador
            if not estado_jogador.concluiu:
                estado_jogador.tempo = time.time() - tempo_inicio_missao

            # D. Renderização da Tela
            retangulo_voltar = desenhar_tela_principal(
                            tela, (LARGURA, ALTURA), cenario,
                            estado_jogador, estado_agente,
                            imagens_jogador, imagens_agente
                        )

            # E. Exibir Mensagem Educativa ao Finalizar (A missão permanece ativa até ambos chegarem)[cite: 18]
            if estado_jogador.concluiu and estado_agente.concluiu:
                tipo_foco = cenario.obter_tipo_foco(cenario.objetivo)
                mostrar_mensagem_educativa(tela, (LARGURA, ALTURA), tipo_foco)

            pygame.display.flip()
            relogio.tick(30)

        # 5. Redirecionamento Pós-Missão
        if mostrar_resultados_finais:
            # Integração pendente com resultados.py (Pessoa 5)[cite: 15]
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
