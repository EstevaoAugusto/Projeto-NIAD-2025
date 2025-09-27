import math
import time
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional

# --- Constantes do Jogo ---
JOGADOR_HUMANO = "X"
JOGADOR_IA = "O"
ESPACO_VAZIO = " "

ESTADOS_DE_VITORIA = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
    [0, 4, 8], [2, 4, 6]              # Diagonais
]

def imprimir_titulo_ascii():
    titulo = r"""
==============================================================================================
* *
                      ,--.                  ,---,         ,---,               ,---,          
                    ,--.'|               ,--.' |        '  .' \            .'  .' `\         
                  ,--,:  : |               |  | :        /  ;    '.        ,---.'      \        
               ,`--.'`|  ' :               :  : '       :  :       \       |   |  .`\  |        
               |   :  :  | |               |  ' |       :  |  /\   \      :   : |  '  |        
               :   |   \ | :               '  | |       |  :  ' ;.   :      |   ' '  ;  :        
               |   : '  '; |               |  | :       |  |  ;/  \   \     '   | ;  .  |        
               '   ' ;.   ;               '  : |       '  :  | \  \ ,'     |   | :  |  '        
               |   | | \   |               |  | '       |  |  '  '--'      '   : | /  ;         
               '   : |  ; .'               '  : |       |  :  :            |   | '` ,/          
               |   | '`--'                 ;  |.'       |  | ,'            ;   :  .'            
               '   : |                     '---'         `--''              |   ,.'             
               ;   |.'                                                    '---'              
               '---'                                                                           
* *
==============================================================================================
"""
    print(titulo)

class JogoDaVelha:
    def __init__(self, ia_oponente: 'IA'):
        self.tabuleiro = [ESPACO_VAZIO] * 9
        self.ia = ia_oponente

    """Imprime o estado atual de um tabuleiro."""
    @staticmethod
    def imprimir_tabuleiro(tabuleiro: List[str]):
        print("\n")
        for i in range(3):
            print(f" {tabuleiro[i*3]} | {tabuleiro[i*3+1]} | {tabuleiro[i*3+2]} ")
            if i < 2:
                print("---|---|---")
        print("\n")

    """Verifica se um jogador específico venceu."""
    @staticmethod
    def verificar_vencedor(tabuleiro: List[str], jogador: str) -> bool:
    
        for estado in ESTADOS_DE_VITORIA:
            if all(tabuleiro[i] == jogador for i in estado):
                return True
        return False

    """Verifica se o tabuleiro está completamente preenchido."""
    @staticmethod
    def esta_cheio(tabuleiro: List[str]) -> bool:
        return ESPACO_VAZIO not in tabuleiro

    """Inicia e gerencia uma partida completa."""
    def iniciar_partida(self):
        print("\n--- Jogo da Velha ---")
        poda_status = 'ATIVADA' if self.ia.usar_poda else 'DESATIVADA'
        print(f"Você é '{JOGADOR_HUMANO}'. A IA está jogando com Poda Alfa-Beta: {poda_status}")
        JogoDaVelha.imprimir_tabuleiro(self.tabuleiro)

        while True:
            self._turno_humano()
            JogoDaVelha.imprimir_tabuleiro(self.tabuleiro)
            if self._verificar_fim_de_jogo():
                break

            self._turno_ia()
            JogoDaVelha.imprimir_tabuleiro(self.tabuleiro)
            if self._verificar_fim_de_jogo():
                break

    def _turno_humano(self):
        while True:
            try:
                jogada = int(input("Escolha sua jogada (1-9): ")) - 1
                if 0 <= jogada < 9 and self.tabuleiro[jogada] == ESPACO_VAZIO:
                    self.tabuleiro[jogada] = JOGADOR_HUMANO
                    break
                else:
                    print("Posição inválida ou já ocupada. Tente novamente.")
            except (ValueError, IndexError):
                print("Entrada inválida. Digite um número de 1 a 9.")
    
    def _turno_ia(self):
        print("Computador está tentando ser humano...")
        jogada_ia = self.ia.encontrar_melhor_jogada(self.tabuleiro)
        if jogada_ia is not None:
            self.tabuleiro[jogada_ia] = JOGADOR_IA
            print(f"Computador jogou na posição {jogada_ia + 1}.")

    """Verifica e anuncia o fim do jogo, retornando True se o jogo acabou."""
    def _verificar_fim_de_jogo(self) -> bool:
        
        if JogoDaVelha.verificar_vencedor(self.tabuleiro, JOGADOR_HUMANO):
            print("Parabéns, você venceu!")
            return True
        if JogoDaVelha.verificar_vencedor(self.tabuleiro, JOGADOR_IA):
            print("O computador venceu!")
            return True
        if JogoDaVelha.esta_cheio(self.tabuleiro):
            print("Ixi, deu velha!")
            return True
        return False

class IA:
    """Encapsula toda a lógica da Inteligência Artificial."""
    def __init__(self, usar_poda_alfa_beta: bool = True):
        self.usar_poda = usar_poda_alfa_beta
        self.nos_avaliados = 0

    def encontrar_melhor_jogada(self, tabuleiro: List[str]) -> Optional[int]:
        """Encontra a melhor jogada para a IA, retornando a posição."""
        self.nos_avaliados = 0
        _, melhor_jogada = self._minimax(tabuleiro, 0, -math.inf, math.inf, True)
        return melhor_jogada

    def _minimax(self, tabuleiro: List[str], profundidade: int, alpha: float, beta: float, eh_maximizador: bool) -> Tuple[int, Optional[int]]:
        """Algoritmo MinMax com Poda Alfa-Beta opcional."""
        self.nos_avaliados += 1

        if JogoDaVelha.verificar_vencedor(tabuleiro, JOGADOR_IA):
            return (1, None)
        if JogoDaVelha.verificar_vencedor(tabuleiro, JOGADOR_HUMANO):
            return (-1, None)
        if JogoDaVelha.esta_cheio(tabuleiro):
            return (0, None)

        melhor_pontuacao = (-math.inf, None) if eh_maximizador else (math.inf, None)
        jogador = JOGADOR_IA if eh_maximizador else JOGADOR_HUMANO

        for i in range(9):
            if tabuleiro[i] == ESPACO_VAZIO:
                tabuleiro[i] = jogador
                pontuacao, _ = self._minimax(tabuleiro, profundidade + 1, alpha, beta, not eh_maximizador)
                tabuleiro[i] = ESPACO_VAZIO

                if eh_maximizador:
                    if pontuacao > melhor_pontuacao[0]:
                        melhor_pontuacao = (pontuacao, i)
                    if self.usar_poda:
                        alpha = max(alpha, pontuacao)
                        if beta <= alpha:
                            break
                else: # Minimizador
                    if pontuacao < melhor_pontuacao[0]:
                        melhor_pontuacao = (pontuacao, i)
                    if self.usar_poda:
                        beta = min(beta, pontuacao)
                        if beta <= alpha:
                            break
                            
        return melhor_pontuacao

# --- Funções de Análise e Gráficos ---

def gerar_grafico_barras(titulo: str, label_y: str, dados: List, legendas: List[str]):
    fig, ax = plt.subplots(figsize=(10, 6))
    barras = ax.bar(legendas, dados, color=['#ff6347', '#4682b4'])
    ax.set_ylabel(label_y)
    ax.set_title(titulo)
    ax.set_ylim(0, max(dados) * 1.15 if max(dados) > 0 else 1)
    for barra in barras:
        valor_y = barra.get_height()
        label_texto = f'{valor_y:.5f}' if isinstance(valor_y, float) else str(valor_y)
        plt.text(barra.get_x() + barra.get_width() / 2.0, valor_y, label_texto, va='bottom', ha='center')
    plt.show()

def gerar_grafico_linhas(titulo: str, label_y: str, label_x: str, dados_minmax: List, dados_alfabeta: List):
    fig, ax = plt.subplots(figsize=(10, 6))
    max_len = max(len(dados_minmax), len(dados_alfabeta))
    jogadas = range(1, max_len + 1)
    dados_minmax.extend([dados_minmax[-1] if dados_minmax else 0] * (max_len - len(dados_minmax)))
    dados_alfabeta.extend([dados_alfabeta[-1] if dados_alfabeta else 0] * (max_len - len(dados_alfabeta)))
    ax.plot(jogadas, dados_minmax, marker='o', linestyle='--', label='MinMax Puro')
    ax.plot(jogadas, dados_alfabeta, marker='o', linestyle='-', label='MinMax com Poda Alfa-Beta')
    ax.set_ylabel(label_y)
    ax.set_xlabel(label_x)
    ax.set_title(titulo)
    ax.legend()
    ax.grid(True)
    plt.xticks(jogadas)
    plt.show()

def simular_partida_e_coletar_dados(ia: IA) -> List[int]:
    tabuleiro_simulacao = [ESPACO_VAZIO] * 9
    dados_partida = []
    jogadores = [JOGADOR_HUMANO, JOGADOR_IA]
    idx_jogador_atual = 0

    while not JogoDaVelha.esta_cheio(tabuleiro_simulacao) and \
          not JogoDaVelha.verificar_vencedor(tabuleiro_simulacao, JOGADOR_HUMANO) and \
          not JogoDaVelha.verificar_vencedor(tabuleiro_simulacao, JOGADOR_IA):
        
        jogada = ia.encontrar_melhor_jogada(tabuleiro_simulacao)
        dados_partida.append(ia.nos_avaliados)
        if jogada is not None:
            tabuleiro_simulacao[jogada] = jogadores[idx_jogador_atual]
        idx_jogador_atual = 1 - idx_jogador_atual
    return dados_partida

def executar_analise():
    print("\nIniciando análise de desempenho automática...")
    tabuleiro_vazio = [ESPACO_VAZIO] * 9
    legendas = ['MinMax Puro', 'MinMax com Poda Alfa-Beta']

    ia_minmax = IA(usar_poda_alfa_beta=False)
    tempo_inicio = time.perf_counter()
    ia_minmax.encontrar_melhor_jogada(tabuleiro_vazio)
    tempo_minmax = time.perf_counter() - tempo_inicio
    nos_minmax = ia_minmax.nos_avaliados

    ia_alfabeta = IA(usar_poda_alfa_beta=True)
    tempo_inicio = time.perf_counter()
    ia_alfabeta.encontrar_melhor_jogada(tabuleiro_vazio)
    tempo_alfabeta = time.perf_counter() - tempo_inicio
    nos_alfabeta = ia_alfabeta.nos_avaliados

    print("Simulando partidas para análise de desempenho por jogada...")
    dados_partida_minmax = simular_partida_e_coletar_dados(ia_minmax)
    dados_partida_alfabeta = simular_partida_e_coletar_dados(ia_alfabeta)
    
    nos_podados = nos_minmax - nos_alfabeta
    percentual_poda = (nos_podados / nos_minmax) * 100 if nos_minmax > 0 else 0

    print("\n" + "="*40 + "\n  ANÁLISE DE DESEMPENHO COMPUTACIONAL\n" + "="*40)
    print(f"| {'Algoritmo':<25} | {'Nós Avaliados':>10} |")
    print("-"*40)
    print(f"| {'MinMax Puro':<25} | {nos_minmax:>10} |")
    print(f"| {'MinMax com Poda Alfa-Beta':<25} | {nos_alfabeta:>10} |")
    print("-"*40)
    print(f"\nTotal de nós 'podados' da árvore: {nos_podados}")
    print(f"Redução de Complexidade (Poda): {percentual_poda:.2f}%\n" + "="*40 + "\n")

    print("Exibindo gráficos de desempenho. Feche cada janela para ver a próxima.")
    gerar_grafico_barras('Análise de Nós Avaliados (Primeira Jogada)', 'Número de Nós', [nos_minmax, nos_alfabeta], legendas)
    gerar_grafico_barras('Análise de Tempo de Execução (Primeira Jogada)', 'Tempo (s)', [tempo_minmax, tempo_alfabeta], legendas)
    gerar_grafico_linhas('Nós Avaliados por Jogada', 'Nós Avaliados', 'Número da Jogada', dados_partida_minmax, dados_partida_alfabeta)

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    while True:
        imprimir_titulo_ascii()
        print("--- MENU PRINCIPAL ---")
        print("1. Jogar contra a IA Otimizada (Com Poda Alfa-Beta)")
        print("2. Jogar contra a IA Padrão (Sem Poda Alfa-Beta)")
        print("3. Gerar Gráficos de Desempenho")
        print("4. Sair")
        
        escolha = input("Digite sua escolha (1, 2, 3 ou 4): ")

        if escolha == '1':
            ia = IA(usar_poda_alfa_beta=True)
            jogo = JogoDaVelha(ia)
            jogo.iniciar_partida()
        elif escolha == '2':
            ia = IA(usar_poda_alfa_beta=False)
            jogo = JogoDaVelha(ia)
            jogo.iniciar_partida()
        elif escolha == '3':
            executar_analise()
        elif escolha == '4':
            print("Obrigado por jogar!")
            break
        else:
            print("Opção inválida. Por favor, escolha 1, 2, 3 ou 4.")
