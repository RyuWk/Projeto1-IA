def manhattan(posicao, objetivo):
    linha, coluna = posicao
    linha_objetivo, coluna_objetivo = objetivo

    return abs(linha - linha_objetivo) + abs(coluna - coluna_objetivo)


