from collections import deque
import time


def reconstruir_caminho(pais, inicio, objetivo):
    """
    Reconstrói o caminho encontrado pela busca.

    O dicionário 'pais' guarda de qual posição
    cada estado foi alcançado.
    """

    caminho = []
    atual = objetivo

    while atual is not None:
        caminho.append(atual)
        atual = pais[atual]

    caminho.reverse()

    return caminho


def calcular_custo(cenario, caminho):
    """
    Calcula o custo total do caminho.

    O custo da posição inicial não é contabilizado,
    pois nenhum movimento foi realizado para chegar nela.
    """

    custo_total = 0

    for posicao in caminho[1:]:
        custo_total += cenario.obter_custo(posicao)

    return custo_total


def bfs(cenario):
    """
    Busca em Largura (Breadth-First Search).

    Retorna um dicionário contendo:
    - caminho
    - custo
    - passos
    - estados_expandidos
    - estados_gerados
    - fronteira_max
    - tempo_execucao
    """

    inicio_tempo = time.perf_counter()

    inicio = cenario.inicio
    objetivo = cenario.objetivo

    # A BFS utiliza uma fila (FIFO)
    fronteira = deque([inicio])

    # Guarda os estados que já foram descobertos
    visitados = {inicio}

    # Guarda o estado anterior de cada posição
    pais = {
        inicio: None
    }

    estados_expandidos = 0
    estados_gerados = 1
    fronteira_max = 1

    while fronteira:

        # Remove o primeiro elemento da fila
        atual = fronteira.popleft()

        estados_expandidos += 1

        # Verifica se chegou ao objetivo
        if atual == objetivo:

            caminho = reconstruir_caminho(
                pais,
                inicio,
                objetivo
            )

            custo = calcular_custo(
                cenario,
                caminho
            )

            passos = len(caminho) - 1

            fim_tempo = time.perf_counter()

            return {
                "caminho": caminho,
                "custo": custo,
                "passos": passos,
                "estados_expandidos": estados_expandidos,
                "estados_gerados": estados_gerados,
                "fronteira_max": fronteira_max,
                "tempo_execucao": fim_tempo - inicio_tempo
            }

        # Obtém os vizinhos através do Cenario
        for vizinho in cenario.obter_vizinhos(atual):

            # Só adiciona posições ainda não descobertas
            if vizinho not in visitados:

                visitados.add(vizinho)

                pais[vizinho] = atual

                fronteira.append(vizinho)

                estados_gerados += 1

        # Guarda o maior tamanho da fila
        if len(fronteira) > fronteira_max:
            fronteira_max = len(fronteira)

    # Caso não exista caminho até o objetivo
    fim_tempo = time.perf_counter()

    return {
        "caminho": [],
        "custo": 0,
        "passos": 0,
        "estados_expandidos": estados_expandidos,
        "estados_gerados": estados_gerados,
        "fronteira_max": fronteira_max,
        "tempo_execucao": fim_tempo - inicio_tempo
    }