from ambiente.celula import (
    CUSTOS_PADRAO,
    DIFICIL,
    FOCO,
    GRAMA,
    LIVRE,
    OBSTACULO,
)


class Cenario:
    """
    Representa o ambiente de simulação como uma matriz bidimensional
    (ver Seção 2.3 do enunciado do projeto).

    Cada posição válida da matriz corresponde a um estado possível do
    agente. Os movimentos entre células adjacentes (cima, baixo, esquerda
    e direita) definem implicitamente um grafo de busca, em que:
    - os nós correspondem às posições válidas da matriz;
    - as arestas correspondem aos movimentos possíveis entre posições
      vizinhas;
    - o peso de cada aresta corresponde ao custo de deslocamento até a
      célula de destino.

    Não é necessário construir esse grafo explicitamente: os vizinhos de
    cada posição são gerados dinamicamente por 'obter_vizinhos'.
    """

    def __init__(self, nome, mapa, inicio, focos, objetivo=None,
                 custos=None, decoracoes=None):
        """
        nome: identificação do cenário (ex: "Cenário 1 - Quintal").
        mapa: matriz (lista de listas) com os tipos de célula definidos
              em ambiente.celula (LIVRE, GRAMA, DIFICIL, OBSTACULO, FOCO).
        inicio: tupla (linha, coluna) com a posição inicial da missão.
        focos: dicionário {(linha, coluna): tipo_do_foco} com todos os
               possíveis focos de dengue presentes no cenário. 'tipo_do_foco'
               é uma das constantes de ambiente.celula (PNEU, VASO, etc.).
        objetivo: posição do foco escolhido como objetivo da missão. Se
                  omitido, utiliza-se o primeiro foco cadastrado.
        custos: dicionário opcional {tipo_de_celula: custo}. Caso não seja
                informado, utiliza-se ambiente.celula.CUSTOS_PADRAO.
        decoracoes: dicionário opcional {(linha, coluna): nome_da_imagem}
                    usado apenas para fins visuais (ex: diferenciar um
                    obstáculo "árvore" de um obstáculo "parede").
        """

        self.nome = nome
        self.mapa = mapa
        self.linhas = len(mapa)
        self.colunas = len(mapa[0]) if self.linhas > 0 else 0

        self.custos = dict(custos) if custos is not None else dict(CUSTOS_PADRAO)
        self.focos = dict(focos)
        self.decoracoes = dict(decoracoes) if decoracoes else {}

        self.inicio = tuple(inicio)

        if objetivo is not None:
            self.objetivo = tuple(objetivo)
        elif self.focos:
            self.objetivo = next(iter(self.focos))
        else:
            self.objetivo = None

        self._validar()

    def _dentro_dos_limites(self, posicao):
        linha, coluna = posicao
        return 0 <= linha < self.linhas and 0 <= coluna < self.colunas

    def _validar(self):
        if self.linhas == 0 or self.colunas == 0:
            raise ValueError(f"O cenário '{self.nome}' possui uma matriz vazia.")

        for linha in self.mapa:
            if len(linha) != self.colunas:
                raise ValueError(
                    f"O cenário '{self.nome}' possui uma matriz irregular "
                    "(todas as linhas devem ter o mesmo número de colunas)."
                )

        if not self._dentro_dos_limites(self.inicio):
            raise ValueError(
                f"Posição inicial {self.inicio} fora dos limites do "
                f"cenário '{self.nome}'."
            )
        if self.mapa[self.inicio[0]][self.inicio[1]] == OBSTACULO:
            raise ValueError(
                f"A posição inicial {self.inicio} não pode ser um obstáculo."
            )

        if not self.focos:
            raise ValueError(
                f"O cenário '{self.nome}' precisa ter ao menos um foco de dengue."
            )

        for posicao, tipo in self.focos.items():
            if not self._dentro_dos_limites(posicao):
                raise ValueError(
                    f"Foco '{tipo}' em {posicao} está fora dos limites do "
                    f"cenário '{self.nome}'."
                )
            if self.mapa[posicao[0]][posicao[1]] != FOCO:
                raise ValueError(
                    f"A posição {posicao} precisa estar marcada como FOCO "
                    "na matriz para receber um tipo de foco."
                )

        if self.objetivo not in self.focos:
            raise ValueError(
                f"O objetivo {self.objetivo} precisa ser um dos focos "
                f"cadastrados no cenário '{self.nome}'."
            )

        tipos_de_terreno_com_custo = {
            tipo for tipo in (LIVRE, GRAMA, DIFICIL, FOCO) if tipo in self.custos
        }
        if len(tipos_de_terreno_com_custo) < 2:
            raise ValueError(
                f"O cenário '{self.nome}' precisa ter pelo menos dois tipos "
                "de terreno com custos diferentes."
            )

    def definir_objetivo(self, posicao):
        """Seleciona qual foco cadastrado será o objetivo da missão."""
        posicao = tuple(posicao)
        if posicao not in self.focos:
            raise ValueError(
                f"{posicao} não é um foco cadastrado no cenário '{self.nome}'."
            )
        self.objetivo = posicao

    def obter_vizinhos(self, posicao):
        """
        Retorna as posições vizinhas válidas (função sucessora do espaço de
        estados): posições dentro dos limites da matriz e que não sejam
        obstáculo.
        """

        linha, coluna = posicao

        movimentos = [
            (-1, 0),    # cima
            (1, 0),     # baixo
            (0, -1),    # esquerda
            (0, 1),     # direita
        ]

        vizinhos = []

        for movimento_linha, movimento_coluna in movimentos:
            nova_posicao = (linha + movimento_linha, coluna + movimento_coluna)

            if self._dentro_dos_limites(nova_posicao):
                nova_linha, nova_coluna = nova_posicao
                if self.mapa[nova_linha][nova_coluna] != OBSTACULO:
                    vizinhos.append(nova_posicao)

        return vizinhos

    def obter_custo(self, posicao):
        """Retorna o custo de deslocamento até a célula informada."""

        terreno = self.mapa[posicao[0]][posicao[1]]

        if terreno == OBSTACULO:
            raise ValueError(
                f"Obstáculos não possuem custo de deslocamento: {posicao}."
            )

        return self.custos[terreno]

    def obter_tipo_foco(self, posicao):
        """Retorna o tipo do foco de dengue (pneu, vaso, etc.) em 'posicao',
        ou None caso a posição não seja um foco cadastrado."""

        return self.focos.get(tuple(posicao))

    def teste_objetivo(self, posicao):
        """Verifica se a posição informada corresponde ao foco selecionado
        como objetivo da missão."""

        return tuple(posicao) == self.objetivo

    def __repr__(self):
        return (
            f"Cenario('{self.nome}', {self.linhas}x{self.colunas}, "
            f"inicio={self.inicio}, objetivo={self.objetivo}, "
            f"focos={list(self.focos.keys())})"
        )
