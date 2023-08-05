from pathlib import Path
import os
import base64
from typing import Dict

from locksey.errors import (
    PasswordDoesNotExistError,
    PathAlreadyExistsError,
    PasswordAlreadyExistsError,
)

from locksey.file import json_from_file, dump_json


CONFIG_PATH = str(Path.home() / ".locksey")
CURRENT_PATH = os.getcwd()


def base64encode(decoded: str) -> str:
    return base64.b64encode(decoded.encode("utf-8")).decode("utf-8")


def base64decode(encoded: str) -> str:
    return base64.b64decode(encoded.encode("utf-8")).decode("utf-8")


def get_config() -> Dict[str, str]:
    if not os.path.exists(CONFIG_PATH):
        return {}

    return json_from_file(CONFIG_PATH)


def set_config(config: Dict[str, str]) -> None:
    dump_json(CONFIG_PATH, config)


def is_child_path(child: str, parent: str) -> bool:
    parent_path = os.path.abspath(parent)
    child_path = os.path.abspath(child)
    return parent_path == os.path.commonpath([parent_path, child_path])


def set_password(password: str) -> None:
    config = get_config()

    if CURRENT_PATH in config:
        raise PasswordAlreadyExistsError

    for path in config:
        if is_child_path(CURRENT_PATH, path):
            raise PathAlreadyExistsError

    config[CURRENT_PATH] = base64encode(password)

    set_config(config)


def rm_password() -> None:
    config = get_config()

    try:
        _ = config[CURRENT_PATH]
        del config[CURRENT_PATH]
    except KeyError as error:
        raise PasswordDoesNotExistError from error

    set_config(config)


def get_password() -> str:
    config = get_config()

    try:
        return base64decode(config[CURRENT_PATH])
    except KeyError as error:
        raise PasswordDoesNotExistError from error
