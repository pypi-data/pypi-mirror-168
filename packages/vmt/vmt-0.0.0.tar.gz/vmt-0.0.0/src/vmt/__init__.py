#!/usr/bin/env python3
import sys

from .build import build_main, update_library
from .config import NoBaseDir, NoBaseDirExists, UserSettings
from .media import watch
from .options import get_opts
from .search import main_search
from .system import browse_base


__license__ = 'GPL-v3.0'

program_name = 'vmt'


def process_opts(user, user_args):
    """
    Opts handler for main
    """
    if user_args.build:
        print('Building')
        return build_main(user, user_args)
    elif user_args.browse:
        return browse_base(user)
    elif user_args.open is not None:
        print('Opening the given file')
    elif user_args.search is not None:
        return main_search(user, episode=user_args.search)
    elif user_args.track is not None:
        return main_search(user, episode=user_args.track, track=True)
    elif user_args.update:
        return update_library(user, user_args)
    elif user_args.watch or user_args.latest:
        return watch(user, latest=user_args.latest)
    else:
        return update_library(user, user_args)


def main():
    """
    Command line application to view and track media
    """
    # Set and get command line args
    user_args = get_opts(program_name)

    try:
        # Creates a UserSettings object. This will be used by various
        # function to access file paths, settings, filters, and command
        # line args
        user = UserSettings(program=program_name, cmd_line_args=user_args)
        user_args = user.cmd_args
    except (NoBaseDir, NoBaseDirExists) as err:
        print(err)
        return 1

    # Execute the appropriate function based on command line options
    return process_opts(user, user_args=user_args)


if __name__ == '__main__':
    sys.exit(main())
