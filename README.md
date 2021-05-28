# chess-story-generation

The current version of the package `chess-story-generation` reads in pgn-files containing chess moves, analyzes the chess game and exports the results to a file.

In a later version of this package, story generation may be added.

## Installation

Clone this repository and install `chess-story-generation` with `pip`.
```sh
$ git clone git@github.com:TimonSteuer/chess-story-generation.git /path/to/chess-story-generation
$ cd /path/to/chess-story-generation
$ pip install .
```

## Usage

To test the functionalities of `chess-story-generation`, in a terminal run:
```sh
$ cd /path/to/chess-story-generation
$ python -m chess-story
```

This loads in a default pgn-file stored in the package folder, specified in the `config.yaml` file, and exports the results of the analyses to a text-file.

To analyze a different pgn-file, place the pgn-file in a folder of your choosing.
Then adjust the existing `config.yaml` or pass a new one, like this:
```sh
$ python -m chess-story --config /path/to/my_config.yaml
```
