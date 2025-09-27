import math
import time
import matplotlib.pyplot as plt

tabuleiro = [" "] * 9
contador_de_nos = 0
USAR_PODA_ALFA_BETA = True

def imprimir_titulo_ascii():
    titulo = r"""
==============================================================================================
*                                                                                         *
                  ,--.                                                                     
                ,--.'|           ,---,           ,---,                   ,---,             
            ,--,:  : |        ,`--.' |          '  .' \                .'  .' `\           
         ,`--.'`|  ' :        |   :  :         /  ;    '.            ,---.'     \          
         |   :  :  | |        :   |  '        :  :       \           |   |  .`\  |         
         :   |   \ | :        |   :  |        :  |   /\   \          :   : |  '  |         
         |   : '  '; |        '   '  ;        |  :  ' ;.   :         |   ' '  ;  :         
         '   ' ;.    ;        |   |  |        |  |  ;/  \   \        '   | ;  .  |         
         |   | | \   |        '   :  ;        '  :  | \  \ ,'        |   | :  |  '         
         '   : |  ; .'        |   |  '        |  |  '  '--'          '   : | /  ;          
         |   | '`--'          '   :  |        |  :  :                |   | '` ,/           
         '   : |              ;   |.'         |  | ,'                ;   :  .'             
         ;   |.'              '---'           `--''                  |   ,.'               
         '---'                                                       '---'                 
                                                                                                                       
==============================================================================================
"""
    print(titulo)

# --- Funções do Jogo ---

def imprimir_tabuleiro():
    """Imprime o estado atual do tabuleiro global."""
    print("\n")
    for i in range(3):
        print(f" {tabuleiro[i*3]} | {tabuleiro[i*3+1]} | {tabuleiro[i*3+2]} ")
        if i < 2:
            print("---|---|---")
    print("\n")

def verificar_vencedor(t, jogador):
    """Verifica se um jogador específico venceu."""
    estados_de_vitoria = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]              # Diagonais
    ]
    for estado in estados_de_vitoria:
        if all(t[i] == jogador for i in estado):
            return True
    return False

def esta_cheio(t):
    """Verifica se o tabuleiro está completamente preenchido."""
    return " " not in t

def minimax(t, profundidade, alpha, beta, eh_maximizador):
    """Algoritmo MinMax com Poda Alfa-Beta opcional."""
    global contador_de_nos
    contador_de_nos += 1

    if verificar_vencedor(t, "O"): return 1
    if verificar_vencedor(t, "X"): return -1
    if esta_cheio(t): return 0

    if eh_maximizador:
        max_avaliacao = -math.inf
        for i in range(9):
            if t[i] == " ":
                t[i] = "O"
                avaliacao = minimax(t, profundidade + 1, alpha, beta, False)
                t[i] = " "
                max_avaliacao = max(max_avaliacao, avaliacao)
                if USAR_PODA_ALFA_BETA:
                    alpha = max(alpha, avaliacao)
                    if beta <= alpha:
                        break
        return max_avaliacao
    else:
        min_avaliacao = math.inf
        for i in range(9):
            if t[i] == " ":
                t[i] = "X"
                avaliacao = minimax(t, profundidade + 1, alpha, beta, True)
                t[i] = " "
                min_avaliacao = min(min_avaliacao, avaliacao)
                if USAR_PODA_ALFA_BETA:
                    beta = min(beta, avaliacao)
                    if beta <= alpha:
                        break
        return min_avaliacao

def encontrar_melhor_jogada(t):
    """Calcula a melhor jogada para a IA ('O')."""
    melhor_pontuacao = -math.inf
    melhor_jogada = None
    for i in range(9):
        if t[i] == " ":
            t[i] = "O"
            pontuacao = minimax(t, 0, -math.inf, math.inf, False)
            t[i] = " "
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_jogada = i
    return melhor_jogada

def gerar_grafico_barras(titulo, label_y, dados, legendas):
    """Função genérica para criar gráficos de barras."""
    fig, ax = plt.subplots(figsize=(10, 6))
    barras = ax.bar(legendas, dados, color=['#ff6347', '#4682b4'])
    ax.set_ylabel(label_y)
    ax.set_title(titulo)
    ax.set_ylim(0, max(dados) * 1.15 if max(dados) > 0 else 1)
    for barra in barras:
        valor_y = barra.get_height()
        label_texto = f'{valor_y:.5f}' if isinstance(valor_y, float) else str(valor_y)
        plt.text(barra.get_x() + barra.get_width()/2.0, valor_y, label_texto, va='bottom', ha='center')
    plt.show()

def gerar_grafico_linhas(titulo, label_y, label_x, dados_minmax, dados_alfabeta):
    """Cria um gráfico de linhas para comparar dados ao longo do tempo/jogadas."""
    fig, ax = plt.subplots(figsize=(10, 6))
    max_len = max(len(dados_minmax), len(dados_alfabeta))
    jogadas = range(1, max_len + 1)
    
    dados_minmax.extend([dados_minmax[-1]] * (max_len - len(dados_minmax)))
    dados_alfabeta.extend([dados_alfabeta[-1]] * (max_len - len(dados_alfabeta)))
    
    ax.plot(jogadas, dados_minmax, marker='o', linestyle='--', label='MinMax Puro')
    ax.plot(jogadas, dados_alfabeta, marker='o', linestyle='-', label='MinMax com Poda Alfa-Beta')
    ax.set_ylabel(label_y)
    ax.set_xlabel(label_x)
    ax.set_title(titulo)
    ax.legend()
    ax.grid(True)
    plt.xticks(jogadas)
    plt.show()

def simular_partida_e_coletar_dados(usar_poda):
    """Simula uma partida IA vs IA e retorna os nós contados a cada jogada."""
    global USAR_PODA_ALFA_BETA, contador_de_nos
    USAR_PODA_ALFA_BETA = usar_poda
    
    tabuleiro_simulacao = [" "] * 9
    dados_partida = []
    jogador_atual = "X" 

    while not esta_cheio(tabuleiro_simulacao) and not verificar_vencedor(tabuleiro_simulacao, "X") and not verificar_vencedor(tabuleiro_simulacao, "O"):
        contador_de_nos = 0
        
        # A IA sempre joga como se fosse 'O' para encontrar a melhor jogada.
        # Mas a jogada é feita pelo jogador_atual.
        jogada = encontrar_melhor_jogada(tabuleiro_simulacao)

        dados_partida.append(contador_de_nos)
        if jogada is not None:
            tabuleiro_simulacao[jogada] = jogador_atual
        
        jogador_atual = "O" if jogador_atual == "X" else "X"

    return dados_partida

def executar_analise():
    """Executa a análise comparativa completa e gera todos os gráficos."""
    global contador_de_nos, USAR_PODA_ALFA_BETA

    print("\nIniciando análise de desempenho automática...")
    tabuleiro_temporario = [" "] * 9
    legendas = ['MinMax Puro', 'MinMax com Poda Alfa-Beta']

    contador_de_nos = 0
    USAR_PODA_ALFA_BETA = False
    tempo_inicio = time.perf_counter()
    encontrar_melhor_jogada(tabuleiro_temporario)
    tempo_minmax = time.perf_counter() - tempo_inicio
    nos_minmax = contador_de_nos

    # Nós (Alfa-Beta)
    contador_de_nos = 0
    USAR_PODA_ALFA_BETA = True
    tempo_inicio = time.perf_counter()
    encontrar_melhor_jogada(tabuleiro_temporario)
    tempo_alfabeta = time.perf_counter() - tempo_inicio
    nos_alfabeta = contador_de_nos

    # --- Coleta de Dados ao longo de uma partida simulada ---
    print("Simulando partidas para análise de desempenho por jogada...")
    dados_partida_minmax = simular_partida_e_coletar_dados(usar_poda=False)
    dados_partida_alfabeta = simular_partida_e_coletar_dados(usar_poda=True)
    
    # --- Apresentação dos Resultados ---
    nos_podados = nos_minmax - nos_alfabeta
    percentual_poda = (nos_podados / nos_minmax) * 100 if nos_minmax > 0 else 0

    print("\n" + "="*40)
    print("  ANÁLISE DE DESEMPENHO COMPUTACIONAL")
    print("="*40)
    print(f"| {'Algoritmo':<25} | {'Nós Avaliados':>10} |")
    print("-"*40)
    print(f"| {'MinMax Puro':<25} | {nos_minmax:>10} |")
    print(f"| {'MinMax com Poda Alfa-Beta':<25} | {nos_alfabeta:>10} |")
    print("-"*40)
    print(f"\nTotal de nós 'podados' da árvore: {nos_podados}")
    print(f"Redução de Complexidade (Poda): {percentual_poda:.2f}%")
    print("="*40 + "\n")

    # --- Geração dos Gráficos ---
    print("Exibindo gráficos de desempenho. Feche cada janela de gráfico para ver a próxima.")
    gerar_grafico_barras('Análise de Nós Avaliados (Primeira Jogada)', 'Número de Nós da Árvore Avaliados', [nos_minmax, nos_alfabeta], legendas)
    gerar_grafico_barras('Análise de Tempo de Execução (Primeira Jogada)', 'Tempo (segundos)', [tempo_minmax, tempo_alfabeta], legendas)
    gerar_grafico_linhas('Nós Avaliados por Jogada (Partida Simulada)', 'Número de Nós Avaliados', 'Número da Jogada', dados_partida_minmax, dados_partida_alfabeta)

# --- Loop Principal e Menu do Jogo ---

def jogar_partida():
    global tabuleiro
    tabuleiro = [" "] * 9
    
    print("\n--- Jogo da Velha ---")
    print(f"Você é 'X'. A IA está jogando com Poda Alfa-Beta: {'ATIVADA' if USAR_PODA_ALFA_BETA else 'DESATIVADA'}")
    imprimir_tabuleiro()

    while True:
        try:
            jogada = int(input("Escolha sua jogada (1-9): ")) - 1
            if 0 <= jogada < 9 and tabuleiro[jogada] == " ":
                tabuleiro[jogada] = "X"
            else:
                print("Posição inválida ou já ocupada. Tente novamente.")
                continue
        except (ValueError, IndexError):
            print("Entrada inválida. Digite um número de 1 a 9.")
            continue

        imprimir_tabuleiro()

        if verificar_vencedor(tabuleiro, "X"): print("Parabéns, você venceu!"); break
        if esta_cheio(tabuleiro): print("Ixi, deu velha!"); break

        print("Computador está pensando...")
        jogada_ia = encontrar_melhor_jogada(tabuleiro)
        if jogada_ia is not None:
            tabuleiro[jogada_ia] = "O" 
            print(f"Computador jogou na posição {jogada_ia + 1}.")
        
        imprimir_tabuleiro()

        if verificar_vencedor(tabuleiro, "O"): print("O computador venceu!"); break
        if esta_cheio(tabuleiro): print("Ixi, deu velha!"); break

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    
    while True:
        imprimir_titulo_ascii()
        
        print("--- MENU PRINCIPAL ---")
        print("Escolha uma opção:")
        print("1. Jogar contra a IA Otimizada (Com Poda Alfa-Beta)")
        print("2. Jogar contra a IA Padrão (Sem Poda Alfa-Beta)")
        print("3. Gerar Gráficos de Desempenho")
        print("4. Sair")
        
        escolha = input("Digite sua escolha (1, 2, 3 ou 4): ")

        if escolha == '1':
            USAR_PODA_ALFA_BETA = True
            jogar_partida()
        elif escolha == '2':
            USAR_PODA_ALFA_BETA = False
            jogar_partida()
        elif escolha == '3':
            executar_analise()
        elif escolha == '4':
            print("Obrigado por jogar!")
            break
        else:
            print("Opção inválida. Por favor, escolha 1, 2, 3 ou 4.")
