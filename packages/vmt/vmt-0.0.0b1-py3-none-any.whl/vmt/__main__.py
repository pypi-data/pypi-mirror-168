#!/usr/bin/env python3
import sys
from .build import build_main, update_library
from .config import NoBaseDir, NoBaseDirExists, get_user_settings
from .media import watch
from .options import get_opts
from .search import main_search
from .system import browse_base


__license__ = "GPL-v3.0"
__program__ = "vmt"


def process_opts(user, args):
    """
    Opts handler for main
    """
    if args.build:
        print("Building")
        return build_main(user, args)
    elif args.browse:
        return browse_base(user)
    elif args.open is not None:
        print("Opening the given file")
    elif args.search is not None:
        return main_search(user, episode=args.search)
    elif args.track is not None:
        return main_search(user, episode=args.track, track=True)
    elif args.update:
        return update_library(user, args)
    elif args.watch or args.latest:
        return watch(user, latest=args.latest)
    else:
        return update_library(user, args)


def main():
    """
    Command line application to view and track media
    """
    # Set and get command line args
    args = get_opts(__program__)

    try:
        # Creates a UserSettings object. This will be used by various function
        # to access file paths, settings, filters, and command line args
        user, args = get_user_settings(program=__program__, args=args)
    except (NoBaseDir, NoBaseDirExists) as err:
        print(err, file=sys.stderr)
        return 1

    # Execute the appropriate function based on command line options
    return process_opts(user, args=args)


if __name__ == "__main__":
    sys.exit(main())
