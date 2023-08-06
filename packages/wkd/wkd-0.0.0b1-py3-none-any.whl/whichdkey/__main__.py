#!/usr/bin/env python3
import sys
from loadconf import Config
from .options import get_opts
from .define import define_key


__license__ = "GPL-v3.0"
__program__ = "wdk"


def main():
    args = get_opts(__program__)
    user = Config(__program__)
    files = {
        "keys": "binds.json",
        "backup": "old_binds.json",
        "conf": "wdk.conf",
    }
    settings = {
        "prompt_cmd": "dmenu",
        "prompt_args": "",
    }
    create = ["conf", "keys", "backup"]
    user.define_files(user_files=files)
    user.define_settings(settings=settings)
    user.create_files(create_files=create)
    user.read_conf(
        user_settings=list(settings.keys()),
        read_files=["conf"],
    )
    user.store_files(
        files=["keys"],
        json_file=True,
    )
    if args.define:
        return define_key(user)
    elif args.delete:
        pass
    elif args.change:
        pass
    else:
        pass


if __name__ == "__main__":
    sys.exit(main())
