import ssl
from urllib import error, request

from . import exceptions, store_payload, verify_payload


def api_download(cache_root, remote_data, root, headers):
    try:
        payload_data, content_length = yield from simple_api_downloader(
            remote_data, root, headers
        )
        remote_info = {}
        cache_file, cache_id = store_payload.store(
            payload_data, cache_root, root, remote_info
        )
        yield from verify_payload.verify_content(
            content_length,
            len(payload_data),
            cache_file.stat().st_size,
        )
    except exceptions.Fail as err:
        raise exceptions.CommandFail(err)
    except error.HTTPError as err:
        raise exceptions.CommandFail(
            f"{err}: {root}: {err.read().decode(errors='ignore')}"
        )
    except error.URLError as err:
        raise exceptions.CommandFail(f"{err}")
    return cache_file, cache_id


def simple_api_downloader(remote_data: dict, root: str, headers: dict):
    """
    A simple downloader. No resume-support. Will not handle transfer errors.

    Yield protocol:
    - str: log
    - dict: progress

    This is a generator that returns a tuple. You have to call it with ``yield from``
    to receive the return value.

    .. code-block:: pycon

        >>> def gen():
        ...   payload, contentlen = yield from simple_api_downloader(remote_data, root, headers)
        ...   yield from _handle_payload(payload, contentlen)

        >>> for res in gen()
        ...     print(res)

    :returns: A generator
    """

    prefix = remote_data.get("url")
    token = remote_data.get("token")
    insecure = remote_data.get("insecure", False)

    endpoint = f"{prefix}/download/zip/{root}"

    headers["Token"] = token
    req = request.Request(url=endpoint, headers=headers)

    context = ssl.create_default_context()
    if insecure:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    yield {"progress": 0}
    yield f"downloading {root}"
    res = request.urlopen(req, context=context)
    info = res.info()
    if info.get("Content-Type", "") != "application/zip":
        raise exceptions.Fail("Only Content-Type: application/zip is supported")

    content_len = int(info.get("Content-Length", "0"))
    chunk = 1024 * 1024

    yield_progress = content_len > (chunk * 10)
    if yield_progress:
        chunk = content_len // 10

    progress = 0
    buffer = b" "
    payload = b""
    while buffer:
        info = res.info()
        buffer = res.read(chunk)
        payload += buffer
        progress = round(len(payload) / content_len * 100)
        if yield_progress:
            yield {"progress": progress}  # 0-100%
            if progress < 100:
                yield f"downloading {progress}%"  # 0-100%
    if yield_progress:
        yield f"downloading {progress}%"
    yield "download complete"
    return payload, content_len
