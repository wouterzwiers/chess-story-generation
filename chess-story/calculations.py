import chess

from .helpers import get_current_color, get_opponents_color


def get_attacks_info(move_stack):
    squares = list(range(0, 64))
    board = chess.Board()
    attacks_info = {}

    for i, move in enumerate(move_stack):
        attacks_info.setdefault(i, {})
        attacks_info[i]["attack_moves"] = []
        pieces_next_legal_moves = []
        board.push(move)
        board.turn = not board.turn
        next_moves_from_square = move.to_square
        for to_square in squares:
            try:
                board.find_move(
                    from_square=next_moves_from_square,
                    to_square=to_square
                )
                pieces_next_legal_moves.append(
                    chess.Move(
                        from_square=next_moves_from_square,
                        to_square=to_square
                    )
                )
            except ValueError:
                continue
        current_color = get_current_color(board)

        pieces_next_legal_attack_moves = [
            move
            for move in pieces_next_legal_moves
            if board.piece_at(move.to_square)
        ]

        for pieces_next_legal_attack_move in pieces_next_legal_attack_moves:
            if board.is_attacked_by(
                current_color,
                square=pieces_next_legal_attack_move.to_square
            ):
                attacks_info[i]["attack_moves"].append(
                    str(pieces_next_legal_attack_move)
                )

        attacks_info[i]["attacking_move"] = (
            True if attacks_info[i]["attack_moves"]
            else False
        )

        board.turn = not board.turn

    return attacks_info


def get_general_info(moves):
    general_info = {}
    board = chess.Board()
    for i, move in enumerate(moves):
        general_info.setdefault(i, {})
        piece_symbol = board.piece_at(move.from_square).symbol()
        general_info[i]["moving_piece_symbol"] = piece_symbol
        general_info[i]["current_turn"] = "white" if board.turn else "black"
        general_info[i]["current_move"] = str(move)
        board.push(move)
    return general_info


def get_development_values(moves, piece_square_tables):
    development_values = {}
    board = chess.Board()
    for i, move in enumerate(moves):
        development_values.setdefault(i, {})
        piece_symbol = board.piece_at(move.from_square).symbol()
        piece_square_table = piece_square_tables[piece_symbol]
        development_value = (
            piece_square_table[move.to_square]
            - piece_square_table[move.from_square]
        )
        development_values[i]["development_value"] = development_value
        board.push(move)
    return development_values


def get_defenses_info(move_stack):
    defenses_info = {}
    board = chess.Board()
    for i, move in enumerate(move_stack):
        defenses_info.setdefault(i, {})
        opponents_color = get_opponents_color(board)
        piece_is_attacked_before_move = board.is_attacked_by(
            opponents_color,
            square=move.from_square
        )
        board.push(move)
        if not piece_is_attacked_before_move:
            defenses_info[i]["defending_move"] = False
            continue
        piece_is_attacked_after_move = board.is_attacked_by(
            opponents_color,
            square=move.to_square
        )
        defenses_info[i]["defending_move"] = (
            True if not piece_is_attacked_after_move
            else False
        )
    return defenses_info


def get_captures_info(move_stack):
    captures_info = {}
    board = chess.Board()
    for i, move in enumerate(move_stack):
        captures_info.setdefault(i, {})
        captures_info[i]["capturing_move"] = board.is_capture(move)
        captures_info[i]["captured_piece_symbol"] = (
            board.piece_at(move.to_square).symbol() if board.is_capture(move)
            else None
        )
        board.push(move)
    return captures_info
