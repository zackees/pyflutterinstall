"""
Saves the global runtime configuration of the install state.
"""

import json
import os

from appdirs import user_config_dir  # type: ignore

from setenvironment.types import Environment  # type: ignore

CONFIG_DIR = user_config_dir("pyflutterinstall")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def config_save(config: Environment):
    """Dumps the json to disk."""
    # data = config.__dict__
    # data will be the json dump
    assert isinstance(config, Environment)
    data = {}
    data["ENV"] = config.vars
    data["PATH"] = config.paths
    out_content = json.dumps(data, indent=4)
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, encoding="utf-8", mode="w") as filed:
        filed.write(out_content)


def config_load() -> Environment:
    """Loads the json from disk."""
    if not os.path.exists(CONFIG_FILE):
        return Environment(vars={}, paths=[])
    with open(CONFIG_FILE, encoding="utf-8", mode="r") as filed:
        out = json.load(filed)
    return Environment(vars=out.get("ENV", {}), paths=out.get("PATH", []))


def print_config() -> int:
    """Endpoint for printing the current configuration."""
    config = config_load()
    print(f"Config file: {CONFIG_FILE}")
    print(json.dumps(config, indent=4))
    return 0


if __name__ == "__main__":
    print_config()
