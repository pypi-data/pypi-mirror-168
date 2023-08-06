import logging
import os
from pathlib import Path
from typing import Any, MutableMapping, Optional

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore

import toolz
from cerberus import Validator


logger = logging.getLogger("kolo")


schema = {
    "filters": {
        "type": "dict",
        "schema": {
            "include_frames": {"type": "list"},
            "ignore_frames": {"type": "list"},
            "ignore_request_paths": {"type": "list"},
        },
    },
    "wal_mode": {"type": "boolean"},
}
validator = Validator(schema, allow_unknown=False)


def clear_errors(config: MutableMapping[str, Any], errors) -> None:
    for error in errors:
        key = error.document_path[-1]
        if error.info:
            for info in error.info:
                clear_errors(config[key], info)
        else:
            del config[key]


def load_config_from_toml(path: Path) -> MutableMapping[str, Any]:
    try:
        with open(path, "rb") as conf:
            config = tomllib.load(conf)
    except FileNotFoundError:
        logger.info(
            'Kolo config file "%s" not found. Using default configuration.', path
        )
        return {}
    if not validator.validate(config):
        logger.warning("Kolo config file has errors: %s", validator.errors)
        clear_errors(config, validator._errors)
    return config


def create_kolo_directory() -> Path:
    """
    Create the kolo directory and contents if they do not exist

    Returns the path to the .kolo directory for convenience.
    """
    kolo_directory = (Path(os.environ.get("KOLO_PATH", ".")) / ".kolo").resolve()
    kolo_directory.mkdir(parents=True, exist_ok=True)
    with open(kolo_directory / ".gitignore", "w") as gitignore:
        gitignore.write("db.sqlite3\n")
        gitignore.write("db.sqlite3-shm\n")
        gitignore.write("db.sqlite3-wal\n")
        gitignore.write(".gitignore\n")
    return kolo_directory


def merge_or_last(args):
    if all(isinstance(arg, dict) for arg in args):
        return toolz.merge(*args)
    return args[-1]


def load_config(
    extra_config: Optional[MutableMapping[str, Any]] = None
) -> MutableMapping[str, Any]:
    kolo_directory = create_kolo_directory()
    config = load_config_from_toml(kolo_directory / "config.toml")
    if extra_config:
        return toolz.merge_with(merge_or_last, config, extra_config)
    return config
