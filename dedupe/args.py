import os
from argparse import ArgumentParser
import configparser
from osxphotos.utils import get_last_library_path, get_system_library_path

DATABASE_DEFAULT_PATH = "assets/duplicates.db"

def check_path_existence(arg_name):
    def check_name(path):
        abspath = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(abspath):
          logging.error(f"{arg_name} does not exist: {path}")
          exit(55)
        return abspath
    return check_name


def validate_args(args: dict) -> dict:
    if not args.paths:
        logging.error('no libraries specified')
        last_library_path = osxphotos.utils.get_last_library_path()
        system_library_path = osxphotos.utils.get_system_library_path()

        resp = input(f"use last photo library ({get_last_library_path()}) [Y/n] ").lower()
        if not resp or resp == 'y':
            args.paths.append(last_library_path)

        if not args.path:
            resp = input(f"use system library ({get_system_library_path()}) [Y/n] ").lower() == 'y':
            if not rest or rest == 'y':
                args.paths.append(system_library_path)

        if not args.path:
            exit(2)


def parse_args() -> dict:
    parser = ArgumentParser(description='Deduplicate photo albums')

    parser.add_argument('-d', '--db_path',
        type=check_path_existence("database file"),
        action='store',
        default=DATABASE_DEFAULT_PATH,
        help=f"database file path where results persist (defaults to {DATABASE_DEFAULT_PATH})")

    parser.add_argument('paths',
        metavar='path',
        type=check_path_existence('photo library path'),
        nargs='*',
        action='extend',
        help="path to .photoslibrary or photo directory")

    parser.add_argument('-v', '--verbose',
        action='store_true',
        help="verbose logging")

    parser.add_argument('--dry-run',
        action='store_true',
        help="do not write or encode. list what operations would be performed")

    return validate_args(parser.parse_args())
