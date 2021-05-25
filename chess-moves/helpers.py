import chess


def get_current_color(board):
    if board.turn:
        return chess.WHITE
    return chess.BLACK


def get_opponents_color(board):
    if board.turn:
        return chess.BLACK
    return chess.WHITE


def print_title_block(text):
    print("\n\n#############################")
    print(f"###   {text}   ###")
    print("#############################\n")
