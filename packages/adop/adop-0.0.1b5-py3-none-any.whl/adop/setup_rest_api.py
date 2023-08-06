import argparse

from . import restapi


def setup(subparsers: argparse.Action):
    """
    Sub parser for the ``serve-api`` argument.
    """
    setup_v1(subparsers, "serve-api", "REST API latest version")
    setup_v1(subparsers, "serve-api-v1", "REST API v1 (this is the latest version)")


def setup_v1(subparsers: argparse.Action, name: str, help: str):
    """
    Sub parser for the ``serve-api-v1`` argument.
    """
    parser = subparsers.add_parser(name, help=help)
    # parser.add_argument("name", type=str, default="default", help="installation name")
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
        "-b",
        "--bind",
        dest="host",
        type=str,
        default="",
        help="Specify alternate bind address [default: 127.0.0.1]",
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=int,
        default=0,
        help="Specify alternate port [default: 8000]",
    )
    parser.set_defaults(func=restapi.serve)
