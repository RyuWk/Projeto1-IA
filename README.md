# Agente de Combate à Dengue

Projeto desenvolvido para a disciplina de **Inteligência Artificial** da UTFPR – Campus Ponta Grossa.

O projeto consiste no desenvolvimento de uma simulação de combate à dengue utilizando **algoritmos de busca em grafos**. O agente inteligente deve encontrar um caminho entre uma posição inicial e um foco de dengue em um ambiente representado por uma grade 2D.

---

## Objetivo

O objetivo do projeto é aplicar diferentes algoritmos de busca para resolver um problema de navegação em um ambiente com:

- células livres;
- diferentes tipos de terreno;
- diferentes custos de movimentação;
- obstáculos;
- posição inicial;
- foco de dengue (objetivo).

O projeto permite comparar o comportamento e o desempenho dos algoritmos de busca em diferentes cenários.

## Algoritmos implementados

O projeto utiliza quatro algoritmos de busca:

- BFS — Busca em Largura
- DFS — Busca em Profundidade
- Busca Gulosa
- A*

## Heurística
Para os algoritmos Guloso e A*, é utilizada a distância de Manhattan como heurística.

## Objetivo educacional

Além da aplicação dos algoritmos de Inteligência Artificial, o projeto possui caráter educativo relacionado à prevenção da dengue.

A simulação busca apresentar, de forma visual e acessível, informações relacionadas à prevenção e ao combate aos focos do mosquito da dengue.

## Como executar

1. Clonar o repositório
2. Entrar na pasta
3. Instalar Pygame
   
   ```bash
   pip install pygame
   ```
5. Executar o projeto
