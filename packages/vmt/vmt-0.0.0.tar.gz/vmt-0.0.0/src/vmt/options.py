#!/usr/bin/env python3
import argparse


def get_opts(prog_name='vmt'):
    parser = argparse.ArgumentParser(prog=prog_name,
                                     description='''Track and watch your media
                                     library''',
                                     allow_abbrev=False
                                     )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-b', '--build',
                       action='store_true',
                       help='''Build the LIBRARY file. Use -i to build this
                        file interactively.''')
    group.add_argument('-B', '--browse',
                       action='store_true',
                       help='''Browse your BASE_DIR. Set your file manager of
                       choice in the vmt.conf like so:
                           FILE_MANAGER="st -e lf"
                       TUI file managers like lf, nnn, ranger, etc. typically
                       must be started in a terminal emulator.''')
    group.add_argument('-l', '--latest',
                       action='store_true',
                       help='''List your latest tracked anime to resume
                       watching.''')
    group.add_argument('-o', '--open',
                       metavar='FILE',
                       help='''This is a sort of wrapper for mpv which will
                       also track the anime when closed.''')
    group.add_argument('-s', '--search',
                       metavar='FILE',
                       help='''Take a file path and check if it is in your
                       BASE_DIR. Returns 0 if successful or 1 if the file is
                       not in in your BASE_DIR.''')
    group.add_argument('-t', '--track',
                       metavar='FILE',
                       help='''This will track the given FILE. It is best if
                       the the given FILE is the full path to the file. If
                       FILE is a relative path then vmt will attempt to
                       find this file in one of the dirs in your library.
                       If this is not possible you will be informed. The most
                       likely reason that this would happen is that the file
                       is in a dir that has been filtered or it is a new dir
                       that has not been added to your library. In this case
                       update your library and attempt to track again. FILE
                       should be a file somewhere in your BASE_DIR otherwise
                       it will be impossible to track.''')
    group.add_argument('-u', '--update',
                       action='store_true',
                       help='''This will update your library file to match any
                       new or renamed directories. If the directory name has
                       not changed your tracked episodes will carry over. If
                       this is not a new directory but one that has been
                       renamed it will be treated as new and no episode
                       tracking will be carried over.''')
    group.add_argument('-w', '--watch',
                       action='store_true',
                       help='''List all titles in your library. If the chosen
                       title is being tracked then the last tracked episode
                       will begin playing in mpv. This will also turn on
                       tracking for vmt.lua so when you close the video it
                       will be recorded in your library and your history. If
                       this is a title that has no tracked episode then a list
                       of all episodes found in the title's dir will be listed
                       for you to choose from.''')
    parser.add_argument('-c', '--clean',
                        action='store_true',
                        help='''Use this flag with -u if you do not want to
                        keep a backup of your library.''')
    parser.add_argument('-i', '--interactive',
                        action='store_true',
                        help='''Use when building or updating your library.
                        This will make the process interactive. By default vmt
                        tries to set the title of a dir to something sane.
                        See the man page or github for more detailed info about
                        this. If you prefer to set the title value yourself
                        then use this flag. If run in a terminal you will see
                        what the auto generated title would be if you do not
                        enter anything into the dmenu prompt by pessing ESC''')
    parser.add_argument('-r', '--recursive',
                        action='store_true',
                        help='''Use when building to filter directories
                        recursively''')
    args = parser.parse_args()
    return args
