#!/usr/bin/env python3
# import sys
import re
import os
import mimetypes
import json
import pathlib
from platform import system
from .utils import merge_libraries, auto_title
from .prompts import user_choice, InputError, InvalidCmdPrompt


def filter_directory(dir, filters, user_args):
    """
    Filter a directory based on a filter list.
    Optionally recursive
    """
    user_system = system()

    def recursive_filter():
        escape_dir = re.escape(dir)
        for item in filters:
            if user_system == "Windows":
                escape_item = re.escape(item)
                escape_item = f"{escape_item}\\\\"
            else:
                escape_item = re.escape(item)
                escape_item = f"{escape_item}/"

            if re.search(escape_item, escape_dir):
                return True
        return False

    def non_recursive_filter():
        escape_dir = re.escape(dir)
        for item in filters:
            escape_item = re.escape(item)
            if re.search(f"{escape_item}$", escape_dir):
                return True

        return False

    if user_args.recursive:
        if non_recursive_filter():
            return True

        return recursive_filter()

    else:
        return non_recursive_filter()


def is_media(file):
    """
    Test if the given file is a video
    """
    mimestart = mimetypes.guess_type(file)[0]
    if mimestart is not None:
        mimestart = mimestart.split("/")[0]
        if mimestart == "video":
            return True

    return False


def pre_build_check(user, prompt=True):
    """Check for existing user library"""

    # Create a config Path object
    library = pathlib.Path(user.library_file)

    def backup_library():
        library.replace(user.library_bak_file)

    # prompt_user only runs when prompt is True
    def prompt_user():
        # Ask user if they want to backup their library
        # This prompt should only run when building
        # User should not be prompted when updating
        choice = user_choice(["Yes", "No"], user, prompt="Backup library? ")

        if choice == "Yes":
            print("Backing up library")
            backup_library()

        else:
            print("Overwriting library")

    # Check if the file exists, if not create it
    if not library.is_file():
        library.touch()

        # When building this should return True
        # When updating this should return False
        return prompt

    elif prompt:
        if library.stat().st_size != 0:
            prompt_user()

        return True

    else:
        if library.stat().st_size != 0:
            backup_library()
            return True

        else:
            return False


def update_library(user, user_args):
    """Update a user's library"""

    # If the user's library needs to be created or is of size
    # '0' then just build the library, else update
    if not pre_build_check(user, prompt=False):
        return build_main(user, user_args)

    new_library = build_main(user, user_args, write=False)

    with open(user.library_bak_file, "r") as old_data:
        old_library = json.load(old_data)

    merged_library = merge_libraries(
        old_library, new_library, interactive=user_args.interactive
    )

    with open(user.library_file, "w") as new_data:
        json.dump(merged_library, new_data, indent=4)

    return 0


def walk_path(user, user_args):
    """
    Walk the base dir and return a dict with valid dirs and episodes
    Create a valid_dirs dict. This will store the raw dirs
    as the key for a show. Here is the structure
    {
         "path/to/show": {
             "title": "My show",
             "watching": "My show 01.mkv",
             "episodes": [
                 "My show 01.mkv",
                 "My show 02.mkv",
                 "My show 03.mkv",
                 "My show 04.mkv"
             ]
         }
    }
    """

    # Get the user's system
    user_system = system()

    # Create our dict
    valid_dirs = {}

    # For loop to walk the user's base_dir
    for dirpath, _, filenames in os.walk(user.base_dir, followlinks=True):
        # For loop to iterate over the files to ensure the dir
        # contains a video file
        skip_dir = True
        filenames.sort()
        for file in filenames:
            if not is_media(file):
                continue

            else:
                skip_dir = False
                break

        if skip_dir:
            continue

        if user_system == "Windows":
            add_dir = dirpath.replace(f"{user.base_dir}\\", "")

        else:
            add_dir = dirpath.replace(f"{user.base_dir}/", "")

        if filter_directory(add_dir, user.filters, user_args):
            continue

        valid_dirs[add_dir] = {}
        valid_dirs[add_dir]["watching"] = None
        title = auto_title(add_dir, user_system)

        if user_args.interactive:
            title = user_choice([title], user, "Title: ", auto_title=True)

        valid_dirs[add_dir]["title"] = title
        valid_dirs[add_dir]["episodes"] = filenames

    return valid_dirs


def build_main(user, user_args, write=True):
    """
    The main build loop for a user's library
    """

    try:
        pre_build_check(user)
    except (InvalidCmdPrompt, InputError, KeyboardInterrupt) as err:
        print(err)
        return 1

    try:
        valid_dirs = walk_path(user, user_args)

    except (InvalidCmdPrompt, InputError, KeyboardInterrupt) as err:
        print(err)
        return 1

    if write:
        with open(user.library_file, "w") as data:
            json.dump(valid_dirs, data, indent=4)
    else:
        return valid_dirs

    return 0
