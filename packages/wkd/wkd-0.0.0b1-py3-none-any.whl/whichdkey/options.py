#!/usr/bin/env python3
import argparse


def get_opts(prog_name="wdk"):
    parser = argparse.ArgumentParser(
        prog=prog_name,
        description="""
        Which key via dmenu, wdk.
        """,
        allow_abbrev=False,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-d",
        "--define",
        action="store_true",
        help="""
        Interactively define a new keybind/prefix.
        """,
    )
    group.add_argument(
        "-D",
        "--delete",
        action="store_true",
        help="""
        Interactively delete a keybind/prefix.
        """,
    )
    group.add_argument(
        "-c",
        "--change",
        action="store_true",
        help="""
        Interactively change a keybind/prefix.
        """,
    )
    args = parser.parse_args()
    return args
