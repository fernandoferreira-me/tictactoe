"""
TIC TAC TOE - Nosso jogo da velha
"""

import math


# Globals
EMPTY = " "
X_PLAYER = "X"
O_PLAYER = "\u25EF"
SCORES = {
    X_PLAYER: 10,
    O_PLAYER: -10
}
VICTORIES = [
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (1, 5, 9),
    (7, 5, 3),
    (1, 4, 7),
    (2, 5, 8),
    (3, 6, 9)
]

# Functions
def print_board(board):
    """
    Print the board
    """
    print()
    print(f"{board[7]}|{board[8]}|{board[9]}")
    print("-+-+-")
    print(f"{board[4]}|{board[5]}|{board[6]}")
    print("-+-+-")
    print(f"{board[1]}|{board[2]}|{board[3]}")


def has_finished(board):
    """
    Check whether all available moves are made
    """
    return  all([value != EMPTY for value in board.values()])


def check_sequence(positions, board):
    """
    Check if a winner sequency has been filled.
    """
    idx, jdx, hdx = positions
    if board[idx] == board[jdx] == board[hdx] != EMPTY:
        return True
    return False


def get_winner(board):
    """
    Get winner player mark
    """
    for position in VICTORIES:
        if check_sequence(position, board):
            return board[position[0]]
    return None


def has_winner(board):
    """
    Check whether anyone has won
    """
    return any([check_sequence(p, board) for p in VICTORIES])


def reset_board(board):
    """
    Clear board positions for a new round
    """
    for idx in board.keys():
        board[idx] = EMPTY
    return board


def get_available_moves(board):
    """
    Get available moves from board
    """
    return [position for position, turn in board.items() if turn == EMPTY]


def stringfy(items, delimiter=","):
    """
    Transform list of objects in a string with
    the items separated by a delimiter
    """
    return f'{delimiter} '.join([str(item) for item in items])


def play_human(board):
    """
    Ask for human interaction
    """
    try:
        move = int(input("Qual a posição de sua jogada? "))
        available_moves = get_available_moves(board)
        if move not in available_moves:
            print()
            print(f"Jogada já feita ou inválida.\n"
                  f"Posições disponíveis: { stringfy(available_moves) } ")
            move = play_human(board)
    except ValueError:
        print()
        print("Jogada inválida. Jogue de 1 a 9")
        move = play_human(board)
    return move


def compute_score(board):
    """
    Compute score
    """
    if has_winner(board):
        winner = get_winner(board)
        return SCORES[winner]
    if has_finished(board):
        return 0
    return None


def minimax(board, depth, is_maximizing):
    """
    Implement minimax algorithm
    """

    best_score = -math.inf if is_maximizing else math.inf
    for move in get_available_moves(board):
        board[move] = O_PLAYER if is_maximizing else X_PLAYER
        score = compute_score(board)
        if score is not None:
            board[move] = EMPTY
            return score
        score = minimax(board, depth + 1, not is_maximizing)
        board[move] = EMPTY
        if is_maximizing:
            best_score = max(best_score, score)
        else:
            best_score = min(best_score, score)
    return best_score


def get_best_move(board):
    """
    Compute best move for AI player
    """
    moves = {}
    for move in get_available_moves(board):
        board[move] = O_PLAYER
        score = compute_score(board)
        if score is not None:
            return move
        else:
            moves[move] = minimax(board, 1, False)
        board[move] = EMPTY
    return min(moves, key=lambda m: moves[m])


def play_ai(board):
    """
    Robot pick its  move
    """
    return get_best_move(board.copy())


def get_players():
    """
    Get the movement functions for each player
    """
    return {X_PLAYER: play_human, O_PLAYER: play_ai}


def change_turn(mark):
    """
    Change player
    """
    if mark is X_PLAYER:
        return O_PLAYER
    return X_PLAYER


##
# Main method
def game(board):
    """
    Main function, where the game happens
    """
    turn = X_PLAYER
    players = get_players()
    while not has_finished(board):
        print()
        print(f"Jogador {turn} é a sua vez")
        move = players[turn](board=board)
        board[move] = turn
        print_board(board)

        if has_winner(board):
            print("\n O JOGO ACABOU \n")
            print(f"***** {turn} ganhou ****")
            break
        turn = change_turn(turn)

    restart = input("Gostaria de jogar novamente? (y/n) ")
    if restart in ('y', 'Y'):
        board = reset_board(board)
        game(board)


# Run as a script
if __name__ == "__main__":
    theBoard = {idx: EMPTY for idx in range(1, 10)}
    game(theBoard)
