import yaml


class Config():
    def __init__(self, path):
        with open(path) as file:
            self._config = yaml.load(file, Loader=yaml.SafeLoader)

    def __getitem__(self, key):
        """Get an item from `_config`."""
        return self._config[key]
