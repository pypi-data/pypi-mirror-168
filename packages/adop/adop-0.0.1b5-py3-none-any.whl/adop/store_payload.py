import json
import logging
import pathlib
import re
import shutil
import time
from hashlib import sha256

from .exceptions import Fail

logger = logging.getLogger(__name__)


def store(
    bin_data: bytes, cache_root: str, root_from_url: str, remote_info: dict
) -> "tuple[~pathlib.Path, str]":
    """
    Store the received payload to disk and add a json-file with meta-data.

    :return: The path to ``post_data.zip`` and the sha256-sum of the file.

    """
    if len(bin_data) == 0:
        raise Fail("Missing post data")
    if not root_from_url:
        raise Fail("HTTP url <root> not found")
    cache = sha256(bin_data).hexdigest()
    tmp = pathlib.Path.cwd().joinpath(cache_root, cache)
    tmp.mkdir(parents=True, exist_ok=True)
    metadata = {
        "sha256": cache,
        "root_from_url": root_from_url,
        "content_len": len(bin_data),
        "remote_info": remote_info,
    }
    post_metadata = tmp.joinpath("post_metadata.json")
    post_metadata.write_text(json.dumps(metadata, indent=2))
    post_data = tmp.joinpath("post_data.zip")
    post_data.write_bytes(bin_data)
    auto_delete = tmp.joinpath("auto_delete.json")
    auto_delete.write_text(
        json.dumps({"root": root_from_url, "auto_delete": 1, "serial": time.time()})
    )
    return post_data, cache


def find_file_from_headers(
    cache_root: str, headers: dict
) -> "tuple[~pathlib.Path, str]":
    """
    Find a pre stored zip file using the Zip-Sha256 header from request object

    :return: The path to ``post_data.zip`` and the sha256-sum of the file.
    """
    cache = headers.get("Zip-Sha256", "")
    if not cache:
        raise Fail("header Zip-Sha256 is missing")
    if not re.search(r"\W", cache) is None:
        raise Fail("header Zip-Sha256 is not sha256")
    if not len(cache) == 64:
        raise Fail("header Zip-Sha256 is not sha256")

    tmp = pathlib.Path.cwd().joinpath(cache_root, cache, "post_data.zip")
    if not tmp.exists():
        raise Fail("file not found")
    return tmp, cache


def auto_delete(cache_root: str, keep_on_disk: int, handle_root: str = ""):
    """
    Delete old cache dirs and its content.

    :return: A generator
    """
    tmp = pathlib.Path.cwd().joinpath(cache_root)
    file_list = tmp.glob("*/auto_delete.json")
    root_mapping = {}

    for file in file_list:
        info = json.loads(file.read_text())
        if info["auto_delete"] == 1:
            root = info["root"]
            serial = info["serial"]
            if root not in root_mapping:
                root_mapping[root] = {}
            root_mapping[root][serial] = file.parent

    for root, serial_mapping in root_mapping.items():
        if handle_root and not handle_root == root:
            continue
        for serial in sorted(serial_mapping.keys(), reverse=True)[keep_on_disk:]:
            path = serial_mapping[serial]
            yield f"auto remove expired cache {path.name}"
            logger.info(f"auto remove expired cache {path}")
            shutil.rmtree(path, ignore_errors=True)
