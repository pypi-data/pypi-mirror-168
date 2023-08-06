import pathlib
import zipfile

from .exceptions import Fail


def extract_root_dir_name(filename: pathlib.Path) -> str:
    """
    Return the base dir of the zip archive. This will fail if
    zip-file has multiple folders in root.
    """

    if not zipfile.is_zipfile(filename):
        raise Fail("Data is not a Zip-file")

    zipobj = zipfile.ZipFile(filename, allowZip64=True)
    dirs = list(zipfile.Path(zipobj).iterdir())
    if len(dirs) != 1:
        raise Fail("ZipFile: only one root dir is permitted")

    if not dirs[0].is_dir():
        raise Fail("ZipFile: root is not a dir")

    return dirs[0].name


def unpack(filename: pathlib.Path, deploy_root: str, transform_root=""):
    """
    Unpack the zip archive to deploy_root and delete any files
    from the deploy_root that is not found in zip archive.
    Folders will not be deleted, but this may change.

    :return: A generator
    """

    yield "verify zip data"

    zip_root = extract_root_dir_name(filename)
    name_start = len(zip_root) + 1

    yield f"zip root: {repr(zip_root)}"
    if transform_root:
        yield f"transform root to: {transform_root}"
    else:
        transform_root = zip_root

    # ensure folders exists
    unpack_root = pathlib.Path(deploy_root)
    unpack_root.mkdir(parents=True, exist_ok=True)

    yield {"progress": 0}
    yield "unpack zip data"

    zipobj = zipfile.ZipFile(filename, allowZip64=True)
    all_zip_names = list(name[name_start:] for name in zipobj.namelist())
    yield_progress = []  # used to yield progress status in rest api response
    if len(all_zip_names) > 100:
        yield_progress = all_zip_names[:: len(all_zip_names) // 10]

    # unpacking files
    for zip_name in all_zip_names:
        if zip_name in yield_progress:
            progress = yield_progress.index(zip_name)
            yield {"progress": progress * 5}  # 0-50%
            yield f"unpacking {progress * 10}%"  # 0-100%
        zipinfo = zipobj.getinfo(f"{zip_root}/{zip_name}")
        zipinfo.filename = f"{transform_root}/{zip_name}"
        zipobj.extract(zipinfo, unpack_root)

    yield {"progress": 50}
    yield "remove untracked files"

    scan_root = unpack_root.joinpath(transform_root)
    all_unpacked_names = [
        name.relative_to(scan_root).as_posix()
        for name in scan_root.glob("**/*")
        if name.is_file()
    ]
    yield_progress = []  # used to yield progress status in rest api response
    if len(all_unpacked_names) > 100:
        yield_progress = all_unpacked_names[:: len(all_unpacked_names) // 10]

    # scanning for files to delete
    for unpacked_name in all_unpacked_names:
        if unpacked_name in yield_progress:
            progress = yield_progress.index(unpacked_name)
            yield {"progress": 50 + (progress * 5)}  # 50-100%
            yield f"scanning {progress * 10}%"  # 0-100%

        if unpacked_name not in all_zip_names:
            yield f"remove file: {unpacked_name}"
            scan_root.joinpath(unpacked_name).unlink()
    yield {"progress": 100}
