#!/usr/bin/env python3
import json
from promptx import (
    PromptX,
    PromptXCmdError,
    PromptXError,
    PromptXSelectError,
)
from typing import List
import sys


def ask(
    p,
    options: List,
    prompt=None,
    additional_args=None,
    select="first",
    deliminator="\n",
):
    try:
        choice = p.ask(
            options=options,
            prompt=prompt,
            additional_args=additional_args,
            select=select,
            deliminator=deliminator,
        )
    except (
        PromptXCmdError,
        PromptXError,
        PromptXSelectError,
    ) as err:
        print(err, file=sys.stderr)
        sys.exit(1)

    if not choice:
        print("No key, exiting", file=sys.stderr)
        sys.exit(1)

    return choice


def define_key(user, prompt_x=None, recursive=False):
    """
    Define a new keybind/prefix interactively.
    """
    # TODO make a copy of user.stored["keys"] before doing this
    # good oportunity for a util function
    keys = user.stored["keys"] if not recursive else user
    if not prompt_x:
        p = PromptX(
            prompt_cmd=user.settings["prompt_cmd"],
            default_args=user.settings["prompt_args"],
        )
    else:
        p = prompt_x
    prefix = ask(p, options=["Yes", "No"], prompt="Is this a prefix? ")
    if not prefix:
        return 1
    key = ask(p, options=[], prompt="New key: ")
    if len(key) != 1 or key is None:
        return 1
    if prefix == "Yes":
        for k in keys.keys():
            if k.startswith(key):
                ask(
                    p,
                    options=["Okay"],
                    prompt="Use 'wdk -c' to change an already defined key.",
                )
                return 1
    desc = ask(p, options=[], prompt="Enter a description: ")
    add_key = key + " -> " + desc
    if prefix == "No":
        command = ask(p, options=[], prompt="Enter command: ")
        keys[add_key] = command
    elif prefix == "Yes":
        keys[add_key] = {}
        prefix_keys = define_key(user=keys[add_key], prompt_x=p, recursive=True)
        keys[add_key] = prefix_keys
    if recursive:
        return keys
    with open(user.files["keys"], mode="w") as data:
        json.dump(keys, data, indent=4)
    print(keys)
    return 0
