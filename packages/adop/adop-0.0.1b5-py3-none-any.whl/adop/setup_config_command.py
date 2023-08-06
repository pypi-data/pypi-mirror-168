import argparse

from . import parse_config


class register:
    """
    A simple decorator to register sub parsers, but also
    acts as a singelton. Get a list of sub parsers by
    calling `register.subparsers` from the `main` function
    """

    subparsers = []
    "List of registered subparsers"

    @classmethod
    def subparser(cls, w):
        "Register sub parser"
        cls.subparsers.append(w)
        return w


def setup(subparsers: argparse.Action):
    """
    Sub parser for the ``config`` argument.
    """
    setup_v1(subparsers, "config", "Config commands")


def setup_v1(subparsers: argparse.Action, name: str, help: str):
    """
    Sub parser for the ``config-v1`` argument.
    """
    parser = subparsers.add_parser(name, help=help)

    subparsers = parser.add_subparsers(
        title="Commands", description="Additional help for commands: {command} --help"
    )

    # get all registered sub parsers and call its function
    for setup in register.subparsers:
        setup(subparsers)


@register.subparser
def setup_init_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config init`` argument.
    """
    parser = subparsers.add_parser("init", help="init options")

    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.set_defaults(func=parse_config.config_init)


@register.subparser
def setup_set_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config set`` argument.
    """
    parser = subparsers.add_parser("set", help="set option")
    # path_or_file
    parser.add_argument(
        "section",
        type=str,
        default="",
        help="section-name in adop.ini",
    )
    parser.add_argument(
        "option",
        type=str,
        default="",
        help="option-name in adop.ini",
    )
    parser.add_argument(
        "value",
        type=str,
        default="",
        help="new value for given option in given section",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.set_defaults(func=parse_config.config_set)


@register.subparser
def setup_get_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config get`` argument.
    """
    parser = subparsers.add_parser("get", help="get option")
    # path_or_file
    parser.add_argument(
        "section",
        type=str,
        default="",
        help="section-name in adop.ini",
    )
    parser.add_argument(
        "option",
        type=str,
        default="",
        help="option-name in adop.ini",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.add_argument(
        "-a",
        "--all",
        dest="all",
        action="store_true",
        help="Include default values in result",
    )
    parser.set_defaults(func=parse_config.config_get)


@register.subparser
def setup_list_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config list`` argument.
    """
    parser = subparsers.add_parser("list", help="list options")

    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.add_argument(
        "-a",
        "--all",
        dest="all",
        action="store_true",
        help="Include default values in result",
    )
    parser.set_defaults(func=parse_config.config_list)
