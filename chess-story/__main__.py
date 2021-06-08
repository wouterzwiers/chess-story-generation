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
    get_development_values,
    get_ending_info
)
from .generation import generate_sentence
from .helpers import get_full_export_path
from .piece_square_tables import piece_square_tables
from .sentences import sentences


DEFAULT_CONFIG_PATH = r"config.ya?ml"


def main(config_path, silent, force):

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

    # Read in the raw file's last row; only used for ending info.
    with open(pgn_file_path) as file:
        last_row = file.readlines()[-1]

    # Retrieve all moves from game.
    moves = game.mainline_moves()

    # Get all information over the moves from game.
    development_values = get_development_values(moves, piece_square_tables)
    attacks_info = get_attacks_info(moves)
    defenses_info = get_defenses_info(moves)
    captures_info = get_captures_info(moves)
    general_info = get_general_info(moves)
    ending_info = get_ending_info(moves, last_row)

    # Merge all retrieved information together.
    moves_info = {
        i: {
            **general_info[i],
            **development_values[i],
            **attacks_info[i],
            **defenses_info[i],
            **captures_info[i],
            **ending_info[i],
        }
        for i in general_info
    }

    # Generate a story for the moves.
    story = []
    for move_idx, move_info in moves_info.items():
        sentence = generate_sentence(move_idx, move_info, sentences)
        story.append(sentence)

    # Create the folder specified in the config the file will be exported to.
    os.makedirs(config["export_output_folder_path"], exist_ok=True)

    # Pretty-format the information dict, for easier reading.
    pformat_moves_info = pprint.pformat(moves_info)

    # Check if to be exported file already exists.
    full_export_path = get_full_export_path(load_game, config)
    if os.path.isfile(full_export_path):
        if not force:
            raise OSError(
                f"The following file already exists: '{full_export_path}'. "
                "To force overwriting the file, add the 'force' command using "
                "'-f' or '--force'."
            )

    # Export the file.
    with open(full_export_path, "w") as exported_file:
        exported_file.writelines(str(game))
        exported_file.write("\n"*2)
        exported_file.write("\n".join(story))
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
    parser.add_argument("-f", "--force", action="store_true")
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

    main(config_path, args.silent, args.force)
