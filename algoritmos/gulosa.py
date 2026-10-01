import time
import heapq

from algoritmos.heuristica import manhattan

def recriar_caminho(pais, inicio, objetivo):
    caminho = []
    atual = objetivo

    while atual != inicio:
        caminho.append(atual)
        atual = pais[atual]

    caminho.append(inicio)

    caminho.reverse()

    return caminho

def busca_gulosa(cenario, inicio, objetivo):
    inicio_tempo = time.perf_counter()

    fronteira = []
    visitados = set()
    estados_expandidos = []
    estados_gerados = []
    fronteira_max = 1   # tem inicialmento o estado inicial
    pais = {} # dicionário
    descobertos = set()

    heapq.heappush(
        fronteira,
        (manhattan(inicio, objetivo), inicio)
    )
    
    descobertos.add(inicio)

    while fronteira:
        prioridade, atual = heapq.heappop(fronteira)

        if atual in visitados:
            continue

        visitados.add(atual)

        estados_expandidos.append(atual)

        if atual == objetivo:
            caminho = recriar_caminho(pais, inicio, objetivo)

            fim_tempo = time.perf_counter()
            tempo_execucao = fim_tempo - inicio_tempo
            
            return caminho, tempo_execucao, estados_expandidos, estados_gerados, fronteira_max

        vizinhos = cenario.obter_vizinhos(atual)

        for vizinho in vizinhos:
            if vizinho not in descobertos:
                descobertos.add(vizinho)
                estados_gerados.append(vizinho)
                pais[vizinho] = atual

                prioridade = manhattan(vizinho, objetivo)
                heapq.heappush(
                    fronteira,
                    (prioridade, vizinho)
                )

        if len(fronteira) > fronteira_max:
            fronteira_max = len(fronteira)

    return [], 0, estados_expandidos, estados_gerados, fronteira_max   # quando termina sem encontrar o objetivo


