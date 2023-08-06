"""Command-line interface"""
import argparse
from argparse import Action
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Union

from thabala_cli.utils.helpers import partition
from thabala_cli.utils.module_loading import import_string


def lazy_load_command(import_path: str) -> Callable:
    """Create a lazy loader for command"""
    _, _, name = import_path.rpartition(".")

    def command(*args, **kwargs):
        func = import_string(import_path)
        return func(*args, **kwargs)

    command.__name__ = name

    return command


# Used in Arg to enable `None' as a distinct value from "not passed"
_UNSET = object()


class Arg:
    """Class to keep information about command line argument"""

    # pylint: disable=redefined-builtin,unused-argument
    def __init__(
        self,
        flags=_UNSET,
        help=_UNSET,
        action=_UNSET,
        default=_UNSET,
        nargs=_UNSET,
        type=_UNSET,
        choices=_UNSET,
        required=_UNSET,
        metavar=_UNSET,
    ):
        self.flags = flags
        self.kwargs = {}
        for k, v in locals().items():
            if v is _UNSET:
                continue
            if k in ("self", "flags"):
                continue

            self.kwargs[k] = v

    def add_to_parser(self, parser: argparse.ArgumentParser):
        """Add this argument to an ArgumentParser"""
        parser.add_argument(*self.flags, **self.kwargs)


def positive_int(value):
    """Define a positive int type for an argument."""
    try:
        value = int(value)
        if value > 0:
            return value
    except ValueError:
        pass
    raise argparse.ArgumentTypeError(f"invalid positive int value: '{value}'")


# Shared
ARG_PROFILE = Arg(
    (
        "-p",
        "--profile",
    ),
    help="Thabala profile",
    default="default",
)
ARG_LIMIT = Arg(("--limit",), help="Number of items to return")
ARG_OFFSET = Arg(
    ("--offset",),
    help="Number of items to skip before starting to collect the result set",
)
ARG_SERVICE_ID = Arg(
    ("--service-id",),
    help="Service ID",
)
ARG_SERVICE_INSTANCE_ID = Arg(
    ("--service-instance-id",),
    help="Service instance ID",
)
ARG_SERVICE_INSTANCE_ID_REQUIRED = Arg(
    ("--service-instance-id",),
    help="Service instance ID",
    required=True,
)
ARG_USERNAME = Arg(
    ("-u", "--username"),
    help="Username",
)
ARG_KIND = Arg(
    ("--kind",),
    help="Infrastructure YAML kind. Allows multiple values by using comma separated list.",
)
ARG_FILE = Arg(
    ("-f", "--file"),
    help="Path to file",
    required=True,
)


# pylint: disable=inherit-non-class
class ActionCommand(NamedTuple):
    """Single CLI command"""

    name: str
    help: str
    func: Callable
    args: Iterable[Arg]
    description: Optional[str] = None
    epilog: Optional[str] = None


class GroupCommand(NamedTuple):
    """CLI command with subcommands"""

    name: str
    help: str
    subcommands: Iterable
    description: Optional[str] = None
    epilog: Optional[str] = None


CLICommand = Union[ActionCommand, GroupCommand]

GET_COMMANDS = (
    ActionCommand(
        name="infra",
        help="Get infrastructure as a code of the Thabala account",
        func=lazy_load_command("thabala_cli.commands.get_command.infra"),
        args=(
            ARG_PROFILE,
            ARG_KIND,
        ),
    ),
    ActionCommand(
        name="health",
        help="Get health af Thabala account",
        func=lazy_load_command("thabala_cli.commands.get_command.health"),
        args=(ARG_PROFILE,),
    ),
    ActionCommand(
        name="service-instances",
        help="Get Thabala service instances",
        func=lazy_load_command("thabala_cli.commands.get_command.service_instances"),
        args=(
            ARG_PROFILE,
            ARG_LIMIT,
            ARG_OFFSET,
            ARG_SERVICE_ID,
            ARG_SERVICE_INSTANCE_ID,
        ),
    ),
    ActionCommand(
        name="service-instance-users",
        help="Get users of service instances",
        func=lazy_load_command(
            "thabala_cli.commands.get_command.service_instance_users"
        ),
        args=(
            ARG_PROFILE,
            ARG_LIMIT,
            ARG_OFFSET,
            ARG_USERNAME,
            ARG_SERVICE_INSTANCE_ID,
        ),
    ),
    ActionCommand(
        name="users",
        help="Get Thabala users",
        func=lazy_load_command("thabala_cli.commands.get_command.users"),
        args=(
            ARG_PROFILE,
            ARG_LIMIT,
            ARG_OFFSET,
        ),
    ),
    ActionCommand(
        name="version",
        help="Get Thabala account version",
        func=lazy_load_command("thabala_cli.commands.get_command.version"),
        args=(ARG_PROFILE,),
    ),
)

SERVICE_INSTANCE_COMMANDS = (
    ActionCommand(
        name="pause",
        help="Pause a service instance",
        func=lazy_load_command("thabala_cli.commands.service_instance_command.pause"),
        args=(
            ARG_PROFILE,
            ARG_SERVICE_INSTANCE_ID_REQUIRED,
        ),
    ),
    ActionCommand(
        name="resume",
        help="Resume a service instance",
        func=lazy_load_command("thabala_cli.commands.service_instance_command.resume"),
        args=(
            ARG_PROFILE,
            ARG_SERVICE_INSTANCE_ID_REQUIRED,
        ),
    ),
)

thabala_cli_commands: List[CLICommand] = [
    GroupCommand(name="get", help="Get Thabala objects", subcommands=GET_COMMANDS),
    GroupCommand(
        name="service-instance",
        help="Service instance commands",
        subcommands=SERVICE_INSTANCE_COMMANDS,
    ),
    ActionCommand(
        name="apply",
        help="Apply infrastructure component",
        func=lazy_load_command("thabala_cli.commands.apply_command.apply"),
        args=(
            ARG_PROFILE,
            ARG_FILE,
        ),
    ),
    ActionCommand(
        name="version",
        help="Show the version",
        func=lazy_load_command("thabala_cli.commands.version_command.version"),
        args=(),
    ),
]
ALL_COMMANDS_DICT: Dict[str, CLICommand] = {sp.name: sp for sp in thabala_cli_commands}


class ThabalaHelpFormatter(argparse.HelpFormatter):
    """
    Custom help formatter to display help message.
    It displays simple commands and groups of commands in separate sections.
    """

    def _format_action(self, action: Action):
        if isinstance(
            action, argparse._SubParsersAction
        ):  # pylint: disable=protected-access

            parts = []
            action_header = self._format_action_invocation(action)
            action_header = "%*s%s\n" % (self._current_indent, "", action_header)
            parts.append(action_header)

            self._indent()
            subactions = action._get_subactions()  # pylint: disable=protected-access
            action_subcommands, group_subcommands = partition(
                lambda d: isinstance(ALL_COMMANDS_DICT[d.dest], GroupCommand),
                subactions,
            )
            parts.append("\n")
            parts.append("%*s%s:\n" % (self._current_indent, "", "Groups"))
            self._indent()
            for subaction in group_subcommands:
                parts.append(self._format_action(subaction))
            self._dedent()

            parts.append("\n")
            parts.append("%*s%s:\n" % (self._current_indent, "", "Commands"))
            self._indent()

            for subaction in action_subcommands:
                parts.append(self._format_action(subaction))
            self._dedent()
            self._dedent()

            # return a single string
            return self._join_parts(parts)

        return super()._format_action(action)


def get_parser() -> argparse.ArgumentParser:
    """Creates and returns command line argument parser"""
    parser = ArgumentParser(prog="thabala", formatter_class=ThabalaHelpFormatter)
    subparsers = parser.add_subparsers(dest="subcommand", metavar="GROUP_OR_COMMAND")
    subparsers.required = True

    subparser_list = ALL_COMMANDS_DICT.keys()
    sub_name: str
    for sub_name in sorted(subparser_list):
        sub: CLICommand = ALL_COMMANDS_DICT[sub_name]
        _add_command(subparsers, sub)
    return parser


def _sort_args(args: Iterable[Arg]) -> Iterable[Arg]:
    """Sort subcommand optional args, keep positional args"""

    def get_long_option(arg: Arg):
        """Get long option from Arg.flags"""
        return arg.flags[0] if len(arg.flags) == 1 else arg.flags[1]

    positional, optional = partition(lambda x: x.flags[0].startswith("-"), args)
    yield from positional
    yield from sorted(optional, key=lambda x: get_long_option(x).lower())


def _add_command(
    subparsers: argparse._SubParsersAction,
    sub: CLICommand,  # pylint: disable=protected-access
) -> None:
    sub_proc = subparsers.add_parser(
        sub.name,
        help=sub.help,
        description=sub.description or sub.help,
        epilog=sub.epilog,
    )
    sub_proc.formatter_class = RawTextHelpFormatter

    if isinstance(sub, GroupCommand):
        _add_group_command(sub, sub_proc)
    elif isinstance(sub, ActionCommand):
        _add_action_command(sub, sub_proc)
    else:
        raise Exception("Invalid command definition.")


def _add_action_command(sub: ActionCommand, sub_proc: argparse.ArgumentParser) -> None:
    for arg in _sort_args(sub.args):
        arg.add_to_parser(sub_proc)
    sub_proc.set_defaults(func=sub.func)


def _add_group_command(sub: GroupCommand, sub_proc: argparse.ArgumentParser) -> None:
    subcommands = sub.subcommands
    sub_subparsers = sub_proc.add_subparsers(dest="subcommand", metavar="COMMAND")
    sub_subparsers.required = True

    for command in sorted(subcommands, key=lambda x: x.name):
        _add_command(sub_subparsers, command)
