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
from ambiente.cenarios_padrao import obter_cenario
from interface.interface import (
    calcular_tamanho_celula,
    desenhar_tela_principal,
    mostrar_mensagem_educativa,
)
from interface.menu import MenuInicial
from interface.resultados import TelaResultados  # Importação da nova tela de resultados


# --- SEÇÃO 1: ESTRUTURA DE DADOS DOS PARTICIPANTES ---
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

        # Métricas de busca exclusivas do Agente Inteligente (exigidas no trabalho)
        self.estados_expandidos = 0
        self.estados_gerados = 0
        self.fronteira_max = 0

        # Visualização da busca: posições expandidas (em ordem) e quantas já foram exibidas
        self.explorados = []
        self.indice_exploracao = 0


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

    if cenario._dentro_dos_limites(nova_posicao):
        if cenario.mapa[nova_posicao[0]][nova_posicao[1]] != OBSTACULO:
            estado.posicao = nova_posicao
            estado.passos += 1
            estado.custo += cenario.obter_custo(nova_posicao)
            estado.caminho.append(nova_posicao)

            if cenario.teste_objetivo(nova_posicao):
                estado.concluiu = True


# --- SEÇÃO 2: CONTROLADOR PRINCIPAL DA APLICAÇÃO (SEM RECURSÃO) ---
def main():
    pygame.init()

    LARGURA, ALTURA = 1600, 900
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    relogio = pygame.time.Clock()

    rodando_app = True
    while rodando_app:
        # Loop do Menu Inicial
        menu = MenuInicial(LARGURA, ALTURA)
        escolhas_usuario = menu.executar()

        nome_algoritmo = escolhas_usuario["algoritmo"]
        id_cenario = escolhas_usuario["cenario_idx"] + 1

        em_missao = True
        while em_missao:
            pygame.display.set_caption(f"Combate à Dengue - IA ({nome_algoritmo} | Cenário {id_cenario})")
            cenario = obter_cenario(id_cenario)

            # O tamanho das células se ajusta ao cenário para ocupar bem a tela
            tamanho_celula = calcular_tamanho_celula(cenario, (LARGURA, ALTURA))
            todas_imagens = carregar_imagens(tamanho_celula=tamanho_celula)
            imagens_jogador = todas_imagens.copy()
            imagens_jogador["personagem"] = todas_imagens["usuario"]
            imagens_agente = todas_imagens.copy()
            imagens_agente["personagem"] = todas_imagens["agente"]

            # Execução do algoritmo de busca selecionado
            if "BFS" in nome_algoritmo:
                resultado_agente = bfs(cenario)
            elif "DFS" in nome_algoritmo:
                resultado_agente = dfs(cenario)
            elif "Gulosa" in nome_algoritmo:
                resultado_agente = busca_gulosa(cenario)
            elif "A*" in nome_algoritmo:
                resultado_agente = busca_a_estrela(cenario)
            else:
                resultado_agente = bfs(cenario)

            # Instanciação dos participantes
            estado_jogador = EstadoParticipante(cenario.inicio)
            estado_agente = EstadoParticipante(cenario.inicio)

            # População das métricas do Agente a partir do dicionário de retorno da busca
            estado_agente.caminho_pre_calculado = resultado_agente.get("caminho", [])
            estado_agente.tempo_execucao = resultado_agente.get("tempo_execucao", 0.0)
            estado_agente.estados_expandidos = resultado_agente.get("estados_expandidos", 0)
            estado_agente.estados_gerados = resultado_agente.get("estados_gerados", 0)
            estado_agente.fronteira_max = resultado_agente.get("fronteira_max", 0)
            estado_agente.explorados = resultado_agente.get("explorados", [])

            TEMPO_MOVIMENTO_AGENTE = 500
            # A exploração é exibida primeiro, durando no máximo ~3 segundos
            TEMPO_EXPLORACAO = max(15, min(80, 3000 // max(1, len(estado_agente.explorados))))
            inicio_exploracao = pygame.time.get_ticks()
            ultimo_tempo_agente = inicio_exploracao
            tempo_inicio_missao = time.time()

            missao_ativa = True
            mostrar_resultados_finais = False
            retangulo_voltar = pygame.Rect(0, 0, 0, 0)  # Evita erro de variável não declarada

            # --- SEÇÃO 3: LOOP DE SIMULAÇÃO EM TEMPO REAL ---
            while missao_ativa:
                tempo_atual = pygame.time.get_ticks()

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        missao_ativa = False
                        em_missao = False
                        rodando_app = False

                    elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                        if retangulo_voltar.collidepoint(evento.pos):
                            missao_ativa = False
                            em_missao = False  # Retorna ao Menu sem recursão

                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_RETURN and estado_jogador.concluiu and estado_agente.concluiu:
                            mostrar_resultados_finais = True
                            missao_ativa = False

                        elif not estado_jogador.concluiu:
                            processar_movimento_jogador(evento.key, estado_jogador, cenario)
                            if estado_jogador.concluiu:
                                estado_jogador.tempo = time.time() - tempo_inicio_missao

                # Fase 1: revela gradualmente as posições exploradas pela busca
                if estado_agente.indice_exploracao < len(estado_agente.explorados):
                    estado_agente.indice_exploracao = min(
                        len(estado_agente.explorados),
                        (tempo_atual - inicio_exploracao) // TEMPO_EXPLORACAO + 1,
                    )
                    ultimo_tempo_agente = tempo_atual

                # Fase 2: movimentação passo-a-passo do agente no grid
                elif not estado_agente.concluiu:
                    if tempo_atual - ultimo_tempo_agente > TEMPO_MOVIMENTO_AGENTE:
                        if estado_agente.indice_caminho < len(estado_agente.caminho_pre_calculado) - 1:
                            estado_agente.indice_caminho += 1
                            nova_pos = estado_agente.caminho_pre_calculado[estado_agente.indice_caminho]

                            estado_agente.posicao = nova_pos
                            estado_agente.passos += 1
                            estado_agente.custo += cenario.obter_custo(nova_pos)
                            estado_agente.caminho.append(nova_pos)

                            if cenario.teste_objetivo(nova_pos):
                                estado_agente.concluiu = True

                        ultimo_tempo_agente = tempo_atual

                if not estado_jogador.concluiu:
                    estado_jogador.tempo = time.time() - tempo_inicio_missao

                # Renderização da tela principal
                retangulo_voltar = desenhar_tela_principal(
                    tela, (LARGURA, ALTURA), cenario,
                    estado_jogador, estado_agente,
                    imagens_jogador, imagens_agente,
                    tamanho_celula=tamanho_celula, nome_algoritmo=nome_algoritmo
                )

                if estado_jogador.concluiu and estado_agente.concluiu:
                    tipo_foco = cenario.obter_tipo_foco(cenario.objetivo)
                    mostrar_mensagem_educativa(tela, (LARGURA, ALTURA), tipo_foco)

                pygame.display.flip()
                relogio.tick(30)

            # --- SEÇÃO 4: TRANSIÇÃO PARA A TELA DE RESULTADOS ---
            if mostrar_resultados_finais:
                tela_res = TelaResultados(tela, (LARGURA, ALTURA))
                opcao_escolhida = tela_res.exibir(
                    estado_jogador, estado_agente, nome_algoritmo, cenario.nome
                )

                if opcao_escolhida == "REINICIAR":
                    em_missao = True
                elif opcao_escolhida == "MENU":
                    em_missao = False
                elif opcao_escolhida == "SAIR":
                    em_missao = False
                    rodando_app = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()