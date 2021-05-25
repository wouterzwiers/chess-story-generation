import argparse
import chess.pgn
import os
import re

from .config import Config
from .calculations import (
    get_attacks_info,
    get_captures_info,
    get_defenses_info,
    get_general_info,
    get_development_values
)
from .helpers import print_title_block
from .piece_square_tables import piece_square_tables


DEFAULT_CONFIG_PATH = r"config.ya?ml"


def main(config_path):

    config = Config(config_path)

    pgn_file_path = os.path.join(
        config["pgn_gamefiles_folder_path"],
        config["load_game"]
    )

    with open(pgn_file_path) as pgn_file:
        game = chess.pgn.read_game(pgn_file)

    moves = game.mainline_moves()

    development_values = get_development_values(moves, piece_square_tables)
    attacks_info = get_attacks_info(moves)
    defenses_info = get_defenses_info(moves)
    captures_info = get_captures_info(moves)
    general_info = get_general_info(moves)

    # Merge all retrieved information together.
    moves_info = {
        i: {
            **general_info[i],
            **development_values[i],
            **attacks_info[i],
            **defenses_info[i],
            **captures_info[i],
        }
        for i in general_info
    }

    print_title_block("G A M E   I N F O")
    for header, text in game.headers.items():
        print(f"{header}: {text}")

    print_title_block("M O V E   I N F O")
    for move_idx, move_info in moves_info.items():
        print(f"Move {move_idx}: {move_info}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=None)
    args = parser.parse_args()

    if args.config is None:
        for filename in os.listdir():
            if re.match(DEFAULT_CONFIG_PATH, filename):
                config_path = filename
                break
        else:
            raise IOError(
                "Could not find a configuration file in your current "
                " directory. Make sure to pass a path using "
                "'--config /path/to/config.yaml'."
            )
    else:
        config_path = args.config

    main(config_path)
