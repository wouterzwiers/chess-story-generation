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
from .piece_square_tables import piece_square_tables


DEFAULT_CONFIG_PATH = r"config.ya?ml"


def main(config_path):

    config = Config(config_path)

    load_game = config["load_game"]
    pgn_file_path = os.path.join(
        config["pgn_gamefiles_folder_path"],
        load_game
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

    # Create the folder specified in the config the file will be exported to.
    export_output_folder_path = config["export_output_folder_path"]
    os.makedirs(export_output_folder_path, exist_ok=True)

    # Figure out which filename to use for the exported file.
    export_output_filename = config["export_output_filename"]
    if export_output_filename is None:
        export_output_filename = load_game

    # Add the suffix to the filename if necessary.
    export_output_filename_suffix = config["export_output_filename_suffix"]
    if export_output_filename_suffix is not None:
        export_output_filename = (export_output_filename_suffix + ".").join(
            export_output_filename.split(".")
        )

    # Add the prefix to the filename if necessary.
    export_output_filename_prefix = config["export_output_filename_prefix"]
    if export_output_filename_prefix is not None:
        export_output_filename = (
            export_output_filename_prefix
            + export_output_filename
        )

    # Create the full export path.
    full_export_path = os.path.join(
        export_output_folder_path,
        export_output_filename
    )

    # Pretty-format the information dict, for easier reading.
    pformat_moves_info = pprint.pformat(moves_info)

    # Export the file.
    with open(full_export_path, "w") as exported_file:
        exported_file.writelines(str(game))
        exported_file.write("\n"*2)
        exported_file.writelines(pformat_moves_info)


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
