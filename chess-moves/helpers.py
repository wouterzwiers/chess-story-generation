import chess


def get_current_color(board):
    if board.turn:
        return chess.WHITE
    return chess.BLACK


def get_opponents_color(board):
    if board.turn:
        return chess.BLACK
    return chess.WHITE


def get_reversed_piece_square_table(piece_square_table):
    reversed_piece_square_table = [
        piece_square_table[63-i]
        for i in range(0, 64)
    ]
    return reversed_piece_square_table


def print_title_block(text):
    print("\n\n#############################")
    print(f"###   {text}   ###")
    print("#############################\n")
