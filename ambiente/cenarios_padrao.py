"""
Cenários padrão do ambiente de combate à dengue (ver Seção 2.5 do
enunciado do projeto), com três níveis de complexidade:

- Cenário 1 - Quintal (Simples)
- Cenário 2 - Praça (Intermediário)
- Cenário 3 - Bairro (Complexo)

Cada cenário é construído a partir de uma matriz de células (ver
ambiente.celula) e possui posição inicial, um ou mais focos de dengue e
custos de deslocamento por tipo de terreno.

O Cenário 3 foi projetado propositalmente para que o caminho com a menor
quantidade de passos (o que a Busca em Largura encontra) atravesse um
corredor de terreno de difícil acesso e NÃO seja o caminho de menor custo
total -- existe um caminho mais longo em passos, porém mais barato,
contornando esse corredor. Isso permite observar, na análise experimental,
que "menor número de passos" e "menor custo" nem sempre coincidem.
"""

from ambiente.celula import (
    LIVRE as L,
    GRAMA as G,
    DIFICIL as D,
    OBSTACULO as O,
    FOCO as F,
    PNEU,
    VASO,
    GARRAFA,
    BALDE,
    CAIXA_DAGUA,
    CALHA,
    gerar_decoracoes_obstaculos,
)
from ambiente.cenario import Cenario


def criar_cenario_1():
    """Cenário 1 - Quintal (Simples): mapa pequeno, poucos obstáculos,
    poucos caminhos alternativos e custos predominantemente uniformes."""

    mapa = [
        [L, L, L, L, L, L],
        [L, O, O, O, O, L],
        [L, L, L, L, O, L],
        [O, O, O, L, O, L],
        [L, L, L, L, L, L],
        [L, G, G, G, G, F],
    ]

    return Cenario(
        nome="Cenário 1 - Quintal (Simples)",
        mapa=mapa,
        inicio=(0, 0),
        focos={(5, 5): PNEU},
        decoracoes=gerar_decoracoes_obstaculos(mapa),
    )


def criar_cenario_2():
    """Cenário 2 - Praça (Intermediário): ambiente maior, mais obstáculos
    e diferentes possibilidades de caminho até dois focos distintos."""

    mapa = [
        [L, L, L, G, G, L, L, L, G, L],
        [L, O, L, G, O, L, O, L, G, L],
        [L, O, L, L, O, L, O, L, L, L],
        [L, O, O, L, O, L, O, O, O, L],
        [L, L, L, L, L, L, L, L, O, L],
        [G, G, O, O, O, O, L, O, O, L],
        [G, L, L, L, L, O, L, O, L, L],
        [G, L, O, O, L, O, L, L, L, O],
        [L, L, O, F, L, L, O, O, L, F],
        [L, L, O, L, L, L, L, L, L, L],
    ]

    return Cenario(
        nome="Cenário 2 - Praça (Intermediário)",
        mapa=mapa,
        inicio=(0, 0),
        focos={(8, 3): VASO, (8, 9): GARRAFA},
        objetivo=(8, 3),
        decoracoes=gerar_decoracoes_obstaculos(mapa),
    )


def criar_cenario_3():
    """Cenário 3 - Bairro (Complexo): ambiente maior, múltiplos caminhos,
    obstáculos e diferentes tipos de terreno. O caminho mais curto em
    passos atravessa um corredor de terreno de difícil acesso (colunas 4,
    linhas 3-7) e tem custo maior do que um caminho alternativo mais longo
    em passos, porém mais barato, que contorna o corredor pelas frestas
    livres das linhas 3 e 6."""

    mapa = [
        [L, L, L, L, L, L, L, L, L, L, G, G, L, L],
        [L, L, L, L, L, L, L, L, L, L, G, G, L, L],
        [L, L, L, L, L, L, L, L, L, L, L, L, L, L],
        [O, O, O, O, D, O, O, O, L, L, O, O, O, O],
        [L, L, L, L, D, L, L, L, L, L, L, L, L, L],
        [L, L, L, L, D, L, L, L, L, L, L, L, L, L],
        [L, L, O, O, D, O, O, O, O, O, O, O, O, O],
        [L, L, L, L, D, L, L, L, L, L, L, L, L, L],
        [L, L, L, L, L, L, G, G, L, L, L, L, L, L],
        [L, L, G, G, L, L, L, L, L, F, L, L, L, L],
        [L, L, L, L, L, O, O, O, L, L, O, L, L, L],
        [L, L, L, O, L, L, L, O, L, L, L, L, L, F],
    ]

    return Cenario(
        nome="Cenário 3 - Bairro (Complexo)",
        mapa=mapa,
        inicio=(0, 0),
        focos={(9, 9): BALDE, (11, 13): CAIXA_DAGUA},
        objetivo=(9, 9),
        decoracoes=gerar_decoracoes_obstaculos(mapa),
    )


CENARIOS = {
    1: criar_cenario_1,
    2: criar_cenario_2,
    3: criar_cenario_3,
}


def obter_cenario(numero):
    """Retorna uma nova instância do cenário padrão de número 1, 2 ou 3."""

    if numero not in CENARIOS:
        raise ValueError(f"Não existe cenário padrão número {numero}.")

    return CENARIOS[numero]()


if __name__ == "__main__":
    for numero, construtor in CENARIOS.items():
        cenario = construtor()
        print(f"{numero}: {cenario}")
