import configparser
import os
import pathlib
import secrets

from . import hooks

default_config = """[server]
on = 1
host = 127.0.0.1
port = 8000
debug = 0

ssl_on = 0
ssl_certificate =
ssl_certificate_key =

deploy_root = ./work/auto
cache_root = ./work/cache

auth_token =

[auto_delete]
on = 1
keep_on_disk = 5

[auto_fetch]
on = 0
run_at_startup = 1
interval = 7200
sources =
config =

[client]
install = basedir
remote = local

[remote:local]
url = http://${server:host}:${server:port}/api/v1
token = ${server:auth_token}
insecure = 0

[remote:example]
url = https://adop.example.local/api/v1
token = NO
insecure = 0

[install:homedir]
install_root = ~/.adop-autolibs-cache/autolibs
cache_root = ~/.adop-autolibs-cache/cache

[install:basedir]
install_root = ./autolibs
cache_root = ~/.adop-autolibs-cache/cache

[install:parentdir]
install_root = ../autolibs
cache_root = ~/.adop-autolibs-cache/cache

[install:subprojdir]
install_root =  ~/.adop-autolibs-cache/autolibs
cache_root = ~/.adop-autolibs-cache/cache
hook:transform-root = builtins:basedir:add-as-prefix
"""

default_example_config = """
[auto_fetch]
sources = github_example, gitlab_example, self_hosted_example

[github_example]
root = simple-master
check_url = https://api.github.com/repos/fholmer/simple/git/refs/heads/master
payload_url = https://github.com/fholmer/simple/archive/refs/heads/master.zip

[gitlab_example]
root = simple-master
check_url = https://gitlab.com/api/v4/projects/fholmer%%2Fsimple/repository/branches/master
payload_url = https://gitlab.com/fholmer/simple/-/archive/master/simple-master.zip
headers = User-agent: Mozilla/5.0

[self_hosted_example]
root = simple
check_url = https://example.local/api/v1/state/simple
payload_url = https://example.local/api/v1/download/zip/simple
headers = Token: NO, Host: distribute
"""


class Config:
    """
    Read config file or create one if it does not exist.
    """

    def __init__(self, config_file_path: str, host: str, port: int):
        self.config = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation(), delimiters=["="]
        )
        self.config.read_string(default_config)
        config_file = pathlib.Path.cwd().joinpath(config_file_path)
        if not config_file.exists():
            # self.config.read_string(default_example_config)
            # auto generate token
            self.config.set("server", "auth_token", secrets.token_urlsafe(32))
            # ensure that folders exists
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with config_file.open(mode="w") as f:
                self.config.write(f)
        else:
            self.config.read_string(config_file.read_text())
        self.config.read_dict({"auto_fetch": {"config": config_file_path}})
        # if host or port is set from command line arguments these
        # should be used instead of the configured host/port
        if host:
            self.config.set("server", "host", host)
        if port:
            self.config.set("server", "port", str(port))

        self.parse_hooks()

    def parse_hooks(self):
        for section_name, section in self.config.items():
            if section_name.startswith("hook:"):
                pass  # TODO: implement hook sections
            else:
                for option_name, option in section.items():
                    if option_name.startswith("hook:"):
                        hooks.register.hook_entrypoint(
                            section_name, option_name, option
                        )


def parse(config_file: str, host: str, port: int) -> configparser.ConfigParser:
    """
    Return a object that holds config info
    """
    config = Config(config_file, host, port)
    return config.config


def config_init(config_file, cwd):

    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    config_path = pathlib.Path(config_file).expanduser()

    if config_path.exists():
        print(f"Config file: {config_file} already exists.")
    else:
        Config(config_file, None, None)
        print(f"Created {config_file} with default options")


def config_set(section, option, value, config_file, cwd):

    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        allow_no_value=True,
        comment_prefixes=["/"],
        delimiters=["="],
    )
    config.optionxform = lambda option: option
    config_path = pathlib.Path(config_file).expanduser()

    if config_path.exists():
        config.read_string(config_path.read_text())

    if not config.has_section(section):
        config.add_section(section)

    config.set(section, option, value)

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w") as f:
        config.write(f)


def config_get(section, option, config_file, cwd, all):

    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        allow_no_value=True,
        comment_prefixes=["/"],
        delimiters=["="],
    )
    config.optionxform = lambda option: option
    config_path = pathlib.Path(config_file).expanduser()

    if not config_path.exists():
        raise SystemExit("File not found")

    if all:
        config.read_string(default_config)
    config.read_string(config_path.read_text())

    print(config.get(section, option, fallback=""))


def config_list(config_file, cwd, all):

    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        allow_no_value=True,
        comment_prefixes=["/"],
        delimiters=["="],
    )
    config.optionxform = lambda option: option
    config_path = pathlib.Path(config_file).expanduser()

    if not config_path.exists():
        raise SystemExit("File not found")

    if all:
        config.read_string(default_config)
    config.read_string(config_path.read_text())

    for section_name, section in config.items():
        print(f"[{section_name}]")
        for option_name, option in section.items():
            print(f"{option_name} = {option}")
        print("")
