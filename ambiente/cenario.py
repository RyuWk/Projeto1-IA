class Cenario:

    def __init__(self, mapa):
        self.mapa = mapa

    def obter_vizinhos(self, posicao):
        linha, coluna = posicao

        movimentos = [
            (-1, 0),    # cima
            (1, 0),     # baixo
            (0, -1),    # esquerda
            (0, 1)      # direita
        ]

        vizinhos = []

        for movimento_linha, movimento_coluna in movimentos:
            nova_linha = linha + movimento_linha
            nova_coluna = coluna + movimento_coluna

            if 0 <= nova_linha < len(self.mapa) and 0 <= nova_coluna < len(self.mapa[0]):
                if self.mapa[nova_linha][nova_coluna] != 3: # se não for obstáculo
                    vizinhos.append((nova_linha, nova_coluna))

        return vizinhos

    def obter_custo(self, posicao):
        terreno = self.mapa[posicao[0]][posicao[1]]

        custos = {
            0: 1, # caminho
            1: 2, # grama
            2: 4, # terreno dificil
            4: 1  # foco
        }

        return custos[terreno]

