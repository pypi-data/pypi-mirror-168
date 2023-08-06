from argparse import ArgumentParser

from . import (
    __version__,
    exceptions,
    logging,
    setup_config_command,
    setup_rest_api,
    setup_zip_command,
)

setup_list = [setup_rest_api.setup, setup_zip_command.setup, setup_config_command.setup]


def main():
    "Application entrypoint"
    logging.setup_logging()
    global_parser = ArgumentParser(add_help=True)
    global_parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"adop {__version__}",
        help="print version and exit",
    )
    global_parser.set_defaults(func=None)
    subparsers = global_parser.add_subparsers(
        title="Commands", description="Additional help for commands: {command} --help"
    )

    # get all registered sub parsers and call its function
    for setup in setup_list:
        setup(subparsers)

    args = global_parser.parse_args()

    if args.func:
        kwargs = {k: v for k, v in args._get_kwargs() if not k == "func"}
        try:
            args.func(**kwargs)
        except KeyboardInterrupt:
            print("Aborted by user")
        except exceptions.CommandFail as err:
            print(err)
    else:
        global_parser.print_help()


if __name__ == "__main__":
    main()
