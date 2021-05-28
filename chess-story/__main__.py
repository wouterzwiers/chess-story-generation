import argparse
import chess.pgn
import os
import pprint
import re

from .config import Config
from .calculations import (
    get_attacks_info,
    get_captures_info,
    get_defenses_info,
    get_general_info,
    get_development_values
)
from .helpers import get_full_export_path
from .piece_square_tables import piece_square_tables


DEFAULT_CONFIG_PATH = r"config.ya?ml"


def main(config_path, silent):

    # Get the config-file.
    config = Config(config_path)

    # Create the path to the game-file specified in the config.
    load_game = config["load_game"]
    pgn_file_path = os.path.join(
        config["pgn_gamefiles_folder_path"],
        load_game
    )
    

    # Read in the game-file specified in the config.
    with open(pgn_file_path) as pgn_file:
        game = chess.pgn.read_game(pgn_file)

    # Retrieve all moves from game.
    moves = game.mainline_moves()

    # Get all information over the moves from game.
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

    # Create the folder specified in the config the file will be exported to.
    os.makedirs(config["export_output_folder_path"], exist_ok=True)

    # Pretty-format the information dict, for easier reading.
    pformat_moves_info = pprint.pformat(moves_info)

    # Export the file.
    full_export_path = get_full_export_path(load_game, config)
    with open(full_export_path, "w") as exported_file:
        exported_file.writelines(str(game))
        exported_file.write("\n"*2)
        exported_file.writelines(pformat_moves_info)
    
    # Provide user with visual feedback.
    if not silent:
        print("\n### Chess-Story-Generation ###")
        print(f"1. Analyzed file {load_game}.")
        print(f"2. Exported results to {full_export_path}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("-s", "--silent", action="store_true")
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

    main(config_path, args.silent)
