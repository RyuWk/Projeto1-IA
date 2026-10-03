"""
Definições dos tipos de célula, custos de deslocamento e tipos de foco de
dengue utilizados na modelagem da matriz do ambiente (ver Seção 2.3 do
enunciado do projeto).
"""

# --- Tipos de célula do mapa ---
LIVRE = 0       # caminho livre / calçada
GRAMA = 1       # grama
DIFICIL = 2     # terreno de difícil acesso
OBSTACULO = 3   # obstáculo (impede a passagem)
FOCO = 4        # foco de dengue (pode ser selecionado como objetivo da missão)

NOMES_CELULA = {
    LIVRE: "Caminho livre",
    GRAMA: "Grama",
    DIFICIL: "Terreno de difícil acesso",
    OBSTACULO: "Obstáculo",
    FOCO: "Foco de dengue",
}

# Custo padrão de se deslocar para cada tipo de célula, conforme sugestão do
# enunciado (Seção 2.3.1). Cada cenário pode sobrescrever esses valores,
# desde que permaneçam positivos e coerentes com o problema.
CUSTOS_PADRAO = {
    LIVRE: 1,
    GRAMA: 2,
    DIFICIL: 4,
    FOCO: 1,
}

# --- Tipos de foco de dengue (possíveis criadouros do mosquito) ---
PNEU = "pneu"
VASO = "vaso"
GARRAFA = "garrafa"
BALDE = "balde"
CAIXA_DAGUA = "caixa_dagua"
CALHA = "calha"

# Imagem associada a cada tipo de foco (arquivos salvos em ambiente/imagens/)
IMAGEM_FOCO = {
    PNEU: "pneu.png",
    VASO: "vaso.png",
    GARRAFA: "garrafa.png",
    BALDE: "balde.png",
    CAIXA_DAGUA: "tambor.png",
    CALHA: "calha_gota.png",
}

# Mensagem educativa exibida ao final da missão, de acordo com o foco
# alcançado (título curto + orientação de prevenção), conforme Seção 2.4.4.
MENSAGEM_FOCO = {
    PNEU: (
        "Pneu com água acumulada!",
        ("Pneus expostos à chuva acumulam água parada e se tornam criadouros "
        "do mosquito. Fure, cubra ou armazene os pneus em local protegido "
        "da chuva."),
    ),
    VASO: (
        "Vaso de planta com água parada!",
        "Os pratinhos de vasos acumulam água facilmente. Troque a água a ",
        "cada 3 dias ou preencha o pratinho com areia até a borda.",
    ),
    GARRAFA: (
        "Garrafa destampada ao relento!",
        ("Garrafas e outros recipientes abertos acumulam água da chuva. "
        "Mantenha-os tampados ou guardados de boca para baixo quando não "
        "estiverem em uso."),
    ),
    BALDE: (
        "Balde esquecido ao ar livre!",
        ("Baldes sem uso podem acumular água de chuva rapidamente. Guarde-os "
        "virados para baixo ou em local coberto."),
    ),
    CAIXA_DAGUA: (
        "Caixa-d'água ou tambor sem tampa adequada!",
        ("Reservatórios mal vedados são um dos principais criadouros do "
        "Aedes aegypti. Mantenha caixas-d'água e tambores sempre bem "
        "fechados."),
    ),
    CALHA: (
        "Calha entupida com água parada!",
        ("Folhas e sujeira acumuladas nas calhas retêm água da chuva. "
        "Limpe as calhas periodicamente para evitar o acúmulo."),
    ),
}

# Ícones utilizados para representar elementos que não fazem parte do
# cálculo de custo (obstáculos decorativos, início e participantes).
IMAGEM_OBSTACULO = {
    "parede": "obstaculo_parede.png",
    "arvore": "obstaculo_arvore.png",
    "rocha": "rocha.png",
}

IMAGEM_INICIO = "inicio.png"
IMAGEM_USUARIO = "usuario.png"
IMAGEM_AGENTE = "agente.png"


def gerar_decoracoes_obstaculos(mapa):
    """
    Gera, de forma determinística, um dicionário {(linha, coluna): imagem}
    variando a imagem de cada célula de obstáculo entre parede, árvore e
    rocha -- apenas para dar variedade visual ao cenário (não interfere em
    custo ou navegabilidade, que continuam definidos por OBSTACULO).
    """

    variantes = list(IMAGEM_OBSTACULO.values())
    decoracoes = {}

    for linha_idx, linha in enumerate(mapa):
        for coluna_idx, tipo in enumerate(linha):
            if tipo == OBSTACULO:
                indice = (linha_idx + coluna_idx) % len(variantes)
                decoracoes[(linha_idx, coluna_idx)] = variantes[indice]

    return decoracoes
