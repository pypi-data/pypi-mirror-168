import argparse

from . import zip_install, zip_upload


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
    Sub parser for the ``zip`` argument.
    """
    setup_v1(subparsers, "zip", "Zip commands, latest version")
    setup_v1(subparsers, "zip-v1", "Zip commands v1 (this is the latest version)")


def setup_v1(subparsers: argparse.Action, name: str, help: str):
    """
    Sub parser for the ``zip-v1`` argument.
    """
    parser = subparsers.add_parser(name, help=help)

    subparsers = parser.add_subparsers(
        title="Commands", description="Additional help for commands: {command} --help"
    )

    # get all registered sub parsers and call its function
    for setup in register.subparsers:
        setup(subparsers)


@register.subparser
def setup_install_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``zip install`` argument.
    """
    parser = subparsers.add_parser("install", help="Install zip-packages")
    # path_or_file
    parser.add_argument(
        "file",
        type=str,
        default="./requires.ini",
        help="Install from the given requires.ini file",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
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
        "-r",
        "--remote",
        dest="remote",
        type=str,
        default="",
        help="""Install from the given remote.
        Remotes have to be configured in adop.ini. [default: local]""",
    )
    parser.set_defaults(func=zip_install.install)


@register.subparser
def setup_upload_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``zip upload`` argument.
    """
    parser = subparsers.add_parser("upload", help="Upload zip-packages")
    # path_or_file
    parser.add_argument(
        "file",
        type=str,
        default="./requires.ini",
        help="Upload from the given requires.ini file",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
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
        "-r",
        "--remote",
        dest="remote",
        type=str,
        default="",
        help="""Upload from the given remote.
        Remotes have to be configured in adop.ini. [default: local]""",
    )
    parser.set_defaults(func=zip_upload.upload)
