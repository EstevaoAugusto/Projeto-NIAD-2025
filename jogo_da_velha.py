import math

# Representação do tabuleiro
board = [" "] * 9  # 9 espaços vazios

# Flag para ativar/desativar poda alfa-beta
USE_ALPHA_BETA = True

# Função para imprimir o tabuleiro
def print_board():
    print("\n")
    for i in range(3):
        print(" | ".join(board[i*3:(i+1)*3]))
        if i < 2:
            print("---------")
    print("\n")

# Verifica se há um vencedor
def check_winner(b, player):
    win_states = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # colunas
        [0, 4, 8], [2, 4, 6]              # diagonais
    ]
    for state in win_states:
        if all(b[i] == player for i in state):
            return True
    return False

# Verifica se ainda há jogadas possíveis
def is_full(b):
    return all(space != " " for space in b)

# Função minimax com ou sem poda alfa-beta
def minimax(b, depth, alpha, beta, is_maximizing):
    if check_winner(b, "O"):
        return 1
    if check_winner(b, "X"):
        return -1
    if is_full(b):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                eval = minimax(b, depth + 1, alpha, beta, False)
                b[i] = " "
                max_eval = max(max_eval, eval)
                if USE_ALPHA_BETA:
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # poda
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                eval = minimax(b, depth + 1, alpha, beta, True)
                b[i] = " "
                min_eval = min(min_eval, eval)
                if USE_ALPHA_BETA:
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # poda
        return min_eval

# Melhor jogada do computador
def best_move():
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, -math.inf, math.inf, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# Loop principal do jogo
print("Jogo da Velha - Você é X e joga primeiro!")
print("Poda alfa-beta está:", "ATIVADA" if USE_ALPHA_BETA else "DESATIVADA")
print_board()

while True:
    # Jogador humano
    while True:
        try:
            move = int(input("Escolha sua jogada (1-9): ")) - 1
            if move >= 0 and move < 9 and board[move] == " ":
                board[move] = "X"
                break
            else:
                print("Jogada inválida. Tente novamente.")
        except ValueError:
            print("Digite um número válido.")

    print_board()

    if check_winner(board, "X"):
        print("Você venceu!")
        break
    if is_full(board):
        print("Empate!")
        break

    # Jogada do computador
    move = best_move()
    board[move] = "O"
    print("Computador jogou!")
    print_board()

    if check_winner(board, "O"):
        print("O computador venceu!")
        break
    if is_full(board):
        print("Empate!")
        break
