from random import choice


non_piece_generation_keys = ["draw", "checkmate", "resignation"]


def get_generation_key(move_info):
    if move_info.get("game_end_caused_by"):
        return move_info["game_end_caused_by"]
    elif move_info["defending_move"]:
        return "defending"
    elif move_info["attacking_move"]:
        return "attacking"
    elif move_info["capturing_move"]:
        return "capturing"
    return "developing"


def generate_sentence(move_idx, move_info, sentences):
    key = get_generation_key(move_info)
    if key in non_piece_generation_keys:
        sentence = choice(sentences[key])
    else:
        piece_symbol = move_info["moving_piece_symbol"].upper()
        sentence = choice(sentences[piece_symbol][key])
    return f"{move_idx}: {sentence}"
