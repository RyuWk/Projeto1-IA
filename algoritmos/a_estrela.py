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

def busca_a_estrela(cenario, inicio, objetivo):
    inicio_tempo = time.perf_counter()

    fronteira = []
    visitados = set()
    estados_expandidos = []
    estados_gerados = []
    fronteira_max = 1
    pais = {}
    custos = {} # g(n) de cada posição

    custos[inicio] = 0
    prioridade = custos[inicio] + manhattan(inicio, objetivo)

    heapq.heappush(
        fronteira,
        (prioridade, inicio)
    )

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
            novo_custo = custos[atual] + cenario.obter_custo(vizinho)
            
            if vizinho not in custos:
                custos[vizinho] = novo_custo
                pais[vizinho] = atual

                estados_gerados.append(vizinho)

                heuristica = manhattan(vizinho, objetivo)
                prioridade = novo_custo + heuristica

                heapq.heappush(
                    fronteira,
                    (prioridade, vizinho)
                )

            elif novo_custo < custos[vizinho]:
                custos[vizinho] = novo_custo
                pais[vizinho] = atual

                heuristica = manhattan(vizinho, objetivo)
                prioridade = novo_custo + heuristica

                heapq.heappush(
                    fronteira,
                    (prioridade, vizinho)
                )


        if len(fronteira) > fronteira_max:
            fronteira_max = len(fronteira)

    return [], 0, estados_expandidos, estados_gerados, fronteira_max

