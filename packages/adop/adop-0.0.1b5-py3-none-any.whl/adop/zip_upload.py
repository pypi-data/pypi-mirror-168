import json
import os

from . import exceptions, parse_config, store_payload, uploaders, zip_install


def upload(file: str, config: str, cwd: str, remote: str):

    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    abs_conf_path = os.path.abspath(os.path.expanduser(config))
    local_config = parse_config.parse(abs_conf_path, "", "")

    uploader = Uploader(local_config)
    requires_file_data = uploader.parse_requires_file(file)
    install_data = uploader.parse_install_to(requires_file_data)
    requires_data = requires_file_data["requires"]
    remote_data = uploader.parse_remotes(remote)
    uploader.upload(install_data, remote_data, requires_data)


class Uploader(zip_install.RequireFile):
    def upload(self, install_data: dict, remote_data: dict, requires_data: dict):

        keep_on_disk = 0
        if self.config.getboolean("auto_delete", "on"):
            keep_on_disk = self.config.getint("auto_delete", "keep_on_disk")

        _handle_zip = self.gen(install_data, keep_on_disk, remote_data, requires_data)

        try:
            for res in _handle_zip:
                if isinstance(res, dict):
                    if "root" in res:
                        print(f"Requires: {res['root']}")
                    elif "result" in res:
                        print(f"{json.dumps(res)}")
                else:
                    print(f"          {res}")
        except exceptions.CommandFail as err:
            print("          ERROR:")
            raise exceptions.CommandFail(f"             {err}")

    def gen(self, install_data, keep_on_disk, remote_data, requires_data):
        cache_root = install_data["cache_root"]

        for root, shasum in requires_data.items():
            yield {"root": root}  # first result: returns only root
            yield f"Checking {root}={shasum[:15]}..."

            if not shasum.startswith("sha256:"):
                raise exceptions.CommandFail(
                    f"Only sha256 is supported in the [requires] section. ie. {root} = sha256:AABBCC"
                )

            headers = {"Zip-Sha256": shasum.split(":", 1)[1]}

            try:
                cache_file, cache_id = store_payload.find_file_from_headers(
                    cache_root, headers
                )
            except exceptions.Fail:
                raise exceptions.CommandFail(f"{root} with {shasum} not found")
            yield from uploaders.api_upload(cache_file, remote_data, root)
