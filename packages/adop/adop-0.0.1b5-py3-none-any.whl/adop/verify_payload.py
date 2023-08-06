import re

from .exceptions import Fail


def verify_content(header_content_len: int, received_data_len: int, file_len: int):
    """
    Make sure that received data length matches request content length.

    :return: A Generator
    """

    yield "verify data"
    if file_len != received_data_len:
        raise Fail(
            f"file_len {file_len} and received_data_len {received_data_len} differs"
        )
    if file_len != header_content_len:
        raise Fail(
            f"file_len {file_len} and Content-Length {header_content_len} differs"
        )


def verify_root(root_dir_name: str, root_from_url: str):
    """
    Make sure the :term:`root` url path segment matches the :term:`root` zip-file path

    :return: A generator
    """
    yield "verify root dir"
    if not (root_dir_name.lower() == root_from_url.lower()):
        raise Fail(
            f"Zip-file root dir: {root_dir_name} and url <root>: {root_from_url} differs"
        )
    if not verify_safe_basename(root_dir_name):
        raise Fail("Zip-file root dir: found illegal characters")


def verify_safe_basename(text: str) -> bool:
    """
    Returns ``False`` if the text contains reserved windows/linux characters.
    """

    # reserved windows keywords
    reserved_win_keywords = r"(PRN|AUX|CLOCK\$|NUL|CON|COM[1-9]|LPT[1-9])"

    # reserved windows characters
    reserved_win_chars = '[\x00-\x1f\\\\?*:";|/<>]'
    # reserved posix is included in reserved_win_chars. reserved_posix_characters = '/\0'

    extra_chars = "[%$@{}]"

    if not text:
        return False

    return (
        re.search(f"{reserved_win_keywords}|{reserved_win_chars}|{extra_chars}", text)
        is None
    )
