import configparser
import pathlib


def store(
    root_dir_name: str,
    cache_file: pathlib.Path,
    cache_hash: str,
    deploy_root: str,
):
    """
    Generate or update a state file (ini format) that show which zip archive
    that should be extracted to destination directory.
    """

    config, unpack_root, config_file_path = get_config(deploy_root)
    if not config.has_section(root_dir_name):
        config.add_section(root_dir_name)
    config.set(root_dir_name, "source_hash", cache_hash)
    config.set(root_dir_name, "source_file", str(cache_file))
    config.set(
        root_dir_name, "destination_dir", str(unpack_root.joinpath(root_dir_name))
    )
    with config_file_path.open(mode="w") as f:
        config.write(f)


def get_config(
    deploy_root: str,
) -> "tuple[~configparser.ConfigParser, ~pathlib.Path, ~pathlib.Path]":
    """
    Returns the path and contents of ``autodeploystate.ini``.

    :return:
        - A `tuple` of:
            - config object (`~configparser.ConfigParser`)
            - ``deploy_root`` (`~pathlib.Path`)
            - ``config_file_path`` (`~pathlib.Path`)

    """
    unpack_root = pathlib.Path.cwd().joinpath(deploy_root)
    unpack_root.mkdir(parents=True, exist_ok=True)
    config = configparser.ConfigParser()
    config_file_path = unpack_root.joinpath("autodeploystate.ini")
    if config_file_path.exists():
        config.read_string(config_file_path.read_text())
    return config, unpack_root, config_file_path
