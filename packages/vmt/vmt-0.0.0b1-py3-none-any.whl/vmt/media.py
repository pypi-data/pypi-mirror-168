#!/usr/bin/env python3
import json
import os
import sys
from .utils import key_value_list, join
from .prompts import user_choice, InvalidCmdPrompt, InputError
from .system import open_process


def mpv_cmd(item, path=None):
    """Return a command list to feed to system.open_process
    if a path to the item is given it the two will be joined"""

    mpv_list = ["mpv", "--script-opts=vmt-enabled=yes"]

    if path is not None:
        item = os.path.join(path, item)

    mpv_list.append(item)

    return mpv_list


def update_log(log_file, library_file):
    """
    Update user log before displaying
    """

    # Compare log file and library modification
    # times. Only update log if library has been
    # modified more recently than log
    log_time = os.path.getmtime(log_file)
    lib_time = os.path.getmtime(library_file)
    if lib_time < log_time:
        return None

    # Open log and library and load to objects
    with open(log_file, "r") as data:
        log = json.load(data)
    with open(library_file, "r") as data:
        library = json.load(data)

    # Create blank log
    lib_keys = list(library.keys())
    log_keys = list(log.keys())

    # Loop over log file and check if show is
    # still in library
    for dir in log_keys:
        if not dir in lib_keys:
            log.pop(dir)

    with open(log_file, "w+") as data:
        json.dump(log, data, indent=4)


def watch(user, latest=False):
    """
    Watch a show from the user's library
    """

    def ask_user(options, user, prompt):
        """
        Ask a user something and handle any errors, return False if the user
        reponds with nothing or error is caught
        """
        try:
            choice = user_choice(options=options, user=user, prompt=prompt)
        except (InvalidCmdPrompt, InputError, KeyboardInterrupt) as err:
            print(err, sys.stderr)
            return False
        if choice is None:
            return False
        return choice

    # If latest update log so we don't prompt for shows that don't exist anymore
    if latest:
        update_log(
            log_file=user.files["log_file"],
            library_file=user.files["library_file"],
        )
        with open(user.files["log_file"], "r") as data:
            library = json.load(data)
    else:
        with open(user.files["library_file"], "r") as data:
            library = json.load(data)

    # Get vars for prompting user and selecting the desired file to watch
    dirs, values = key_value_list(library)
    _, watching = key_value_list(values, search_key="watching")
    _, titles = key_value_list(values, search_key="title")
    _, episodes = key_value_list(values, search_key="episodes")

    choice = ask_user(options=titles, user=user, prompt="Watch: ")
    if not choice:
        return 1

    index = titles.index(choice)
    path = join(user.settings["base_dir"], dirs[index])

    # If show is does not have a recently watched episode ask user which episode
    # to watch
    if watching[index] is None:
        opts = episodes[index]
        episode = ask_user(options=opts, user=user, prompt="Watch: ")
        if not episode:
            return 1
    else:
        episode = watching[index]

    # Get the mpv command and open start watching the show
    cmd = mpv_cmd(item=episode, path=path)

    open_process(opener=cmd)

    return 0
