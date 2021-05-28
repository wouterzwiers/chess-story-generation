import chess
import os


def get_current_color(board):
    if board.turn:
        return chess.WHITE
    return chess.BLACK


def get_full_export_path(load_game, config):
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
        config["export_output_folder_path"],
        export_output_filename
    )

    return full_export_path


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
