# Projeto Jogo da Velha com IA - NIAD 2025/2

### Uma Análise Comparativa do Algoritmo MinMax com e sem Poda Alfa-Beta

##  Sobre o Projeto

Este projeto foi desenvolvido como parte do processo seletivo de trainees para o **NIAD (Núcleo de Estudos em Inteligência Artificial e Data Science)**. O desafio consistiu em desenvolver uma inteligência artificial invencível para o Jogo da Velha, utilizando o algoritmo MinMax, e, crucialmente, demonstrar quantitativamente o ganho de eficiência computacional obtido com a otimização de Poda Alfa-Beta.

O resultado é um programa interativo que não apenas permite jogar contra duas versões da IA, mas também executa uma análise de desempenho completa, gerando métricas e gráficos que comprovam a eficácia da otimização.

##  Índice

  - [ Sobre o Projeto](#Sobre-o-Projeto)
  - [ Conceitos Implementados](#Conceitos-Implementados)
  - [ Como Executar](#Como-Executar)
  - [ Análise de Desempenho e Estatísticas](#Analise-de-Desempenho-e-Estatisticas)
      - [Métrica Principal: Nós da Árvore Avaliados]
      - [Análise do Gráfico 1: Comparativo de Nós (Primeira Jogada)]
      - [Análise do Gráfico 2: Comparativo de Tempo de Execução]
      - [Análise do Gráfico 3: Desempenho ao Longo de uma Partida]
  - [ Equipe](#equipe)

##  Conceitos Implementados

  - **Algoritmo MinMax:** Implementação do algoritmo clássico para busca em jogos de dois jogadores com soma zero.
  - **Busca Competitiva (Adversarial Search):** Modelagem do Jogo da Velha como uma árvore de decisões onde dois oponentes (Max e Min) tentam otimizar seus resultados.
  - **Otimização com Poda Alfa-Beta:** Implementação da técnica que otimiza o MinMax ao "podar" galhos da árvore de busca que não influenciarão na decisão final.
  - **Análise de Complexidade:** Instrumentação do código com um contador de nós para medir objetivamente a complexidade da busca em cada cenário.
  - **Visualização de Dados:** Uso da biblioteca `Matplotlib` para gerar gráficos comparativos e apresentar os resultados da análise de forma clara e profissional.

##  Como Executar

Para executar o projeto em sua máquina local, siga os passos abaixo.

**Pré-requisitos:**

  - [Python 3.x](https://www.python.org/downloads/)
  - `pip` (gerenciador de pacotes do Python)

**Passos:**

1.  Clone o repositório:
    ```bash
    git clone https://github.com/EstevaoAugusto/Projeto-NIAD-2025
    cd Projeto-NIAD-2025
    ```
2.  Instale as dependências (apenas `matplotlib`):
    ```bash
    pip install matplotlib
    ```
3.  Execute o script principal:
    ```bash
    python jogo_da_velha.py
    ```
4.  O menu principal aparecerá no terminal. Você poderá:
      - Jogar contra as IAs (opções 1 e 2).
      - Gerar a análise de desempenho completa (opção 3).
      - Sair do programa (opção 4).

##  Análise de Desempenho e Estatísticas

O foco deste projeto é **provar quantitativamente** a eficiência da Poda Alfa-Beta. Ao selecionar a opção "Gerar Gráficos de Desempenho", o programa executa uma série de testes e apresenta os seguintes resultados:

### Métrica Principal: Nós da Árvore Avaliados

Em teoria de jogos, a IA explora uma "árvore" de jogadas possíveis. Cada estado do tabuleiro que a IA avalia é chamado de "nó". Contar quantos nós são visitados é a forma mais precisa de medir o esforço computacional (complexidade) do algoritmo. **Menos nós, mais eficiente.**

-----

### Análise do Gráfico 1: Comparativo de Nós (Primeira Jogada)

Este gráfico de barras mostra a quantidade total de nós que cada algoritmo precisou avaliar para decidir qual a melhor primeira jogada em um tabuleiro vazio.

<img width="903" height="551" alt="image" src="https://github.com/user-attachments/assets/94e5e677-8014-412b-ad35-ae62b506d2da" />


**O que observamos?**
A diferença é gritante. O MinMax puro precisa explorar centenas de milhares de possibilidades. Em contrapartida, o MinMax com Poda Alfa-Beta analisa uma fração desse número, atingindo a mesma conclusão (a melhor jogada) com um esforço ordens de magnitude menor.

**Por que isso acontece?**
A Poda Alfa-Beta é "inteligente". Ela para de analisar um caminho de jogadas assim que percebe que ele levará a um resultado pior do que um já encontrado anteriormente. Ela não perde tempo explorando galhos da árvore de decisão que são comprovadamente ruins, resultando nessa drástica redução de nós avaliados.

-----

### Análise do Gráfico 2: Comparativo de Tempo de Execução

Este gráfico traduz a complexidade (número de nós) em um impacto real e mensurável: o tempo que o computador levou para "pensar".

<img width="978" height="577" alt="image" src="https://github.com/user-attachments/assets/069128c1-2081-4e89-a576-9a8d1421af73" />


**O que observamos?**
Assim como no gráfico de nós, o tempo de execução da versão com Poda Alfa-Beta é significativamente menor. A IA otimizada é visivelmente mais rápida.

**Por que isso acontece?**
Esta é a consequência direta da análise anterior. Menos nós para avaliar significa menos operações matemáticas e lógicas para o processador executar. A redução da complexidade do algoritmo se traduz diretamente em uma redução no tempo de processamento.

-----

### Análise do Gráfico 3: Desempenho ao Longo de uma Partida

Este gráfico de linhas é o mais revelador, pois mostra como a eficiência de cada algoritmo se comporta durante uma partida simulada completa.

<img width="945" height="566" alt="image" src="https://github.com/user-attachments/assets/92665561-1e9f-4bc9-a130-dbfadd39d38a" />


**O que observamos?**

1.  **Tendência Decrescente:** Ambas as linhas descem à medida que o jogo avança. Isso é esperado, pois com mais peças no tabuleiro, o número de jogadas futuras possíveis diminui, e a "árvore" de decisão se torna menor.
2.  **Eficiência Consistente:** A linha da Poda Alfa-Beta (azul) se mantém **consistentemente e drasticamente abaixo** da linha do MinMax puro (vermelha) em **todas as etapas** do jogo.

**Por que isso acontece?**
Este gráfico prova que a Poda Alfa-Beta não é apenas uma otimização para o início do jogo, mas sim uma melhoria fundamental que se aplica a qualquer estado do tabuleiro. Em cada turno, ela consegue encontrar e eliminar galhos irrelevantes da árvore de busca, mantendo sua vantagem de eficiência do começo ao fim da partida.

##  Equipe

  - Estevão Augusto da Fonseca Santos
  - Giovane Godoi
  - Luis Gustavo
  - Marco Franco
  - Arthur Xisto
