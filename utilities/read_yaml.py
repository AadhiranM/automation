import yaml
import os


_config = None  # cache


def read_config():
    global _config

    if _config is None:   # load only once
        base = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(base, "config", "config.yaml")

        with open(path, "r") as f:
            _config = yaml.safe_load(f)

    return _config


def get_config(key=None, default=None):

    config = read_config()

    if key is None:
        return config

    keys = key.split(".")

    value = config

    for k in keys:

        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default

    return value