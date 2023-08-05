import enum
import argparse
import glob
from pathlib import Path
import os
import sys
from getpass import getpass

from typing import Callable

from cryptography.fernet import InvalidToken

from locksey.encrypt import encrypt, decrypt
from locksey.file import str_from_file, dump_str
from locksey.config import get_password, set_password, rm_password
from locksey.errors import (
    PasswordDoesNotExistError,
    PathAlreadyExistsError,
    PasswordAlreadyExistsError,
)


CONFIG_PATH = str(Path.home() / ".locksey")
CURRENT_PATH = os.getcwd()


class Action(str, enum.Enum):
    SET_PASSWD = "setpasswd"
    UNSET_PASSWD = "rmpasswd"
    LOCK = "lock"
    UNLOCK = "unlock"


def rename_path(file_path: str, from_ext: str, to_ext: str) -> str:
    path = Path(file_path)
    parts = list(path.parts)
    renamed_parts = parts[:-1] + [parts[-1].replace(from_ext, to_ext)]
    return os.path.join(*renamed_parts)


def transform_file(
    password: str,
    from_ext: str,
    to_ext: str,
    to_func: Callable[[str, str], str],
) -> None:
    for file_path in glob.glob(f"./**/*.{from_ext}.*", recursive=True):
        from_contents = str_from_file(file_path)

        to_contents = to_func(from_contents, password)
        dump_str(file_path, to_contents)

        to_path = rename_path(file_path, from_ext, to_ext)
        os.rename(file_path, to_path)


def lock_files(password: str) -> None:
    transform_file(password, "unlocked", "locked", encrypt)


def unlock_files(password: str) -> None:
    transform_file(password, "locked", "unlocked", decrypt)


DESCRIPTION = """
Personal CLI utility tool to easily encrypt and decrypt files in a directory.

lock
    Recursively go through the directory encrypt and rename files matching glob ./**/*.unlocked.*
unlock 
    Recursively go through the directory and decrypt and rename files matching glob ./**/*.locked.*
setpasswd
    Store password for current directory in home folder, base64 encoded so you don't have to provide it again
rmpasswd
    Remove stored password for current directory

To change password run 
    1. unlock
    2. rmpasswd if needed 
    3. lock with new password
    4. setpasswd with new password if needed
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m locksey",
        description=DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "action", type=Action, help="Can be one of lock, unlock, setpasswd, rmpasswd"
    )

    args = parser.parse_args()

    try:
        if args.action == Action.SET_PASSWD:
            set_password(getpass())
        elif args.action == Action.UNSET_PASSWD:
            rm_password()
        else:
            try:
                password = get_password()
            except PasswordDoesNotExistError:
                password = getpass()

            if args.action == Action.LOCK:
                lock_files(password)
            elif args.action == Action.UNLOCK:
                unlock_files(password)

        return 0

    except PathAlreadyExistsError:
        print("The current path or the parent of the current path already exists")
    except PasswordDoesNotExistError:
        print("Password does not exist for current directory")
    except PasswordAlreadyExistsError:
        print(
            "Password already set for current directory, use rmpasswd to remove existing password"
        )
    except InvalidToken:
        print("Invalid password")

    parser.print_usage()
    return -1


if __name__ == "__main__":
    sys.exit(main())
