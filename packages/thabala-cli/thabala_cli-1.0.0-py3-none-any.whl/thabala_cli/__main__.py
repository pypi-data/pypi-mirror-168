"""Main executable module"""
import sys

import argcomplete

from thabala_cli import cli_parser
from thabala_cli.exceptions import ThabalaCliException


def main():
    """Main executable function"""
    try:
        parser = cli_parser.get_parser()
        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        args.func(args)
    except ThabalaCliException as err:
        print(err)
        sys.exit(1)


if __name__ == "__main__":
    main()
