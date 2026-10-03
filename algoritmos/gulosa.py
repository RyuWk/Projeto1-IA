import heapq
import time

from algoritmos.heuristica import manhattan


def reconstruir_caminho(pais, objetivo):
    caminho = []
    atual = objetivo
    while atual is not None:
        caminho.append(atual)
        atual = pais.get(atual)
    caminho.reverse()
    return caminho

def calcular_custo(cenario, caminho):
    custo_total = 0
    for posicao in caminho[1:]:
        custo_total += cenario.obter_custo(posicao)
    return custo_total

def busca_gulosa(cenario):
    inicio_tempo = time.perf_counter()

    inicio = cenario.inicio
    objetivo = cenario.objetivo

    fronteira = []
    visitados = set()
    estados_expandidos = 0
    estados_gerados = 1
    fronteira_max = 1

    pais = {inicio: None}
    descobertos = {inicio}

    heapq.heappush(fronteira, (manhattan(inicio, objetivo), inicio))

    while fronteira:
        prioridade, atual = heapq.heappop(fronteira)

        if atual in visitados:
            continue

        visitados.add(atual)
        estados_expandidos += 1

        if atual == objetivo:
            caminho = reconstruir_caminho(pais, objetivo)
            custo = calcular_custo(cenario, caminho)
            passos = len(caminho) - 1
            tempo_execucao = time.perf_counter() - inicio_tempo

            return {
                "caminho": caminho,
                "custo": custo,
                "passos": passos,
                "estados_expandidos": estados_expandidos,
                "estados_gerados": estados_gerados,
                "fronteira_max": fronteira_max,
                "tempo_execucao": tempo_execucao
            }

        for vizinho in cenario.obter_vizinhos(atual):
            if vizinho not in descobertos:
                descobertos.add(vizinho)
                estados_gerados += 1
                pais[vizinho] = atual

                prioridade_vizinho = manhattan(vizinho, objetivo)
                heapq.heappush(fronteira, (prioridade_vizinho, vizinho))

        fronteira_max = max(fronteira_max, len(fronteira))

    tempo_execucao = time.perf_counter() - inicio_tempo
    return {
        "caminho": [], "custo": 0, "passos": 0,
        "estados_expandidos": estados_expandidos,
        "estados_gerados": estados_gerados,
        "fronteira_max": fronteira_max,
        "tempo_execucao": tempo_execucao
    }
