"""
TIC TAC TOE - Nosso jogo da velha
"""

import random


# Globals
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
    print(f"{board[7]}|{board[8]}|{board[9]}")
    print("-+-+-")
    print(f"{board[4]}|{board[5]}|{board[6]}")
    print("-+-+-")
    print(f"{board[1]}|{board[2]}|{board[3]}")

def has_finished(board):
    """
    Check whether all available moves are made
    """
    return  all([value != " " for value in board.values()])


def check_sequency(positions, board):
    """
    Check if a winner sequency has been filled.
    """
    idx, jdx, hdx = positions
    if board[idx] == board[jdx] == board[hdx] != " ":
        return True
    return False


def has_winner(board):
    """
    Check whether anyone has won
    """
    return any([check_sequency(p, board) for p in VICTORIES])


def reset_board(board):
    """
    Clear board positions for a new round
    """
    for idx in board.keys():
        board[idx] = ' '
    return board

def play_human(**args):
    """
    Ask for human interaction
    """
    # pylint: disable=W0613
    try:
        move = int(input("Qual a posição de sua jogada?"))
        if move not in range(1, 10):
            print("Jogada inválida. Jogue de 1 a 9")
            move = play_human()
    except ValueError:
        print("Jogada inválida. Jogue de 1 a 9")
        move = play_human()
    return move

def play_ai(**args):
    """
    Robot pick its  move
    """
    board = args.get('board')
    available_moves = [position for position, turn in board.items()
                       if turn == " "]
    idx = random.randint(0, len(available_moves) - 1)
    return available_moves[idx]


def get_players():
    """
    Get the movement functions for each player
    """
    return {"X": play_human, "O": play_ai}


##
# Main method
def game(board):
    """
    Main function, where the game happens
    """
    turn = "X"
    players = get_players()
    while not has_finished(board):
        print()
        print(f"Jogador {turn} é a sua vez")
        move = players[turn](board=board)

        if board[move] == ' ':
            board[move] = turn
        else:
            print('Posição já jogada')
            continue

        print_board(board)

        if has_winner(board):
            print("\n O JOGO ACABOU \n")
            print(f"***** {turn} ganhou ****")
            break

        if turn == "X":
            turn = "O"
        else:
            turn = "X"

    restart = input("Gostaria de jogar novamente? (y/n)")
    if restart in ('y', 'Y'):
        board = reset_board(board)
        game(board)


# Run as a script
if __name__ == "__main__":
    theBoard = {idx: ' ' for idx in range(1, 10)}
    game(theBoard)
