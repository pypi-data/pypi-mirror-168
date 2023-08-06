#!/usr/bin/env python3
import os
from loadconf import Config


class NoBaseDirExists(Exception):
    """Exception raised when user has a base directory set
    but it does not exist.
    """

    def __init__(self, conf_file, message="ERROR: Base directory is set to"):
        self.file = conf_file
        self.message = message

    def __str__(self):
        return f'{self.message} "{self.file}" which does not exist'


class NoBaseDir(Exception):
    """Exception raised when user has not set a base directory"""

    def __init__(self, conf_file, message="ERROR: Base directory not set in"):
        self.file = conf_file
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} "{self.file}"'


def get_user_settings(program, args):
    # Create user object to read files and get settings
    user = Config(program=program)
    # Define some basic settings, files, etc.
    user_settings = {
        "base_dir": None,
        "prompt_cmd": "fzf",
        "prompt_args": "",
        "file_manager": None,
        "max_history": 20,
        "recursive": False,
        "not_found": False,
        "debug": False,
    }
    config_files = {
        "conf_file": "vmt.conf",
        "log_file": "log.json",
        "filters_file": "filters.conf",
        "library_file": "library.json",
        "library_bak_file": "library.json.bak",
    }
    files = [
        "conf_file",
        "filters_file",
        "library_file",
    ]
    settings = list(user_settings.keys())
    # Fill out user object
    user.define_settings(settings=user_settings)
    user.define_files(user_files=config_files)
    user.create_files(create_files=files)
    user.read_conf(user_settings=settings, read_files=["conf_file"])
    user.store_files(files=["filters_file"])
    # Check that the required settings are defined
    if user.settings["base_dir"] is None:
        raise NoBaseDir(conf_file=user.settings["base_dir"])
    elif not os.path.isdir(user.settings["base_dir"]):
        raise NoBaseDirExists(conf_file=user.settings["base_dir"])
    # Update args based on user settings
    if user.settings["recursive"]:
        args.recursive = True

    return user, args


# class UserSettings:
#     """Class for managing user config files"""

#     # User files containing their location on the system
#     conf_dir = None
#     conf_file = None
#     log_file = None
#     filters_file = None
#     library_file = None
#     library_bak_file = None

#     # Command line args passed by user
#     # This is an argparse object
#     cmd_args = None

#     # User's settings as set in their conf and filters files
#     base_dir = None
#     prompt_cmd = None
#     file_manager = None
#     max_history = None
#     recursive = None
#     not_found = None
#     filters = []

#     def __init__(self, program, cmd_line_args=None):
#         self.add_cmd_args(cmd_line_args=cmd_line_args)
#         self.set_files(program=program)
#         self.read_config()
#         self.set_filters()
#         self.update_cmd_args()
#         self.validate_config()

#     @classmethod
#     def add_cmd_args(cls, cmd_line_args=None):
#         cls.cmd_args = cmd_line_args

#     @classmethod
#     def set_files(cls, program=None):
#         """Return user config directory and config_files dict"""

#         cls.conf_dir = appdirs(program)
#         config_files = {
#             "conf_file": "vmt.conf",
#             "log_file": "log.json",
#             "filters_file": "filters.conf",
#             "library_file": "library.json",
#             "library_bak_file": "library.json.bak",
#         }

#         for key, value in config_files.items():
#             value = os.path.join(cls.conf_dir, value)
#             setattr(cls, key, value)

#     @classmethod
#     def read_config(cls):
#         """Read user config files and update user_args"""

#         with open(cls.conf_file) as conf:
#             reader = csv.reader(
#                 conf, delimiter="=", escapechar="\\", quoting=csv.QUOTE_NONE
#             )

#             config_settings = ["base_dir", "prompt_cmd", "max_history", "not_found"]

#             for row in reader:
#                 if len(row) > 2:
#                     raise csv.Error(f"Too many fields on row: {row}")

#                 setting_name = row[0].strip().lower()
#                 setting_value = row[1].strip()

#                 if setting_name == "file_manager":
#                     setting_value = split(setting_value)
#                 elif setting_name == "recursive":
#                     try:
#                         setting_value = eval(setting_value.capitalize())
#                     except NameError as err:
#                         msg = (
#                             f'ERROR: "{setting_name}" must be set to "True" or "False"'
#                         )
#                         print(f"{msg}\n\t{err}", file=sys.stderr)
#                 elif not setting_name in config_settings:
#                     continue

#                 setattr(cls, setting_name, setting_value)

#     @classmethod
#     def set_filters(cls):
#         """Read the users filters_file into the filters attribute"""
#         with open(cls.filters_file) as filter:
#             for line in filter:
#                 cls.filters.append(line.rstrip("\n"))

#     @classmethod
#     def update_cmd_args(cls):
#         """Update the cmd_args object based on user settings"""

#         if cls.recursive:
#             cls.cmd_args.recursive = True

#         if cls.base_dir is None or cls.base_dir == "":
#             raise NoBaseDir(cls.conf_file)
#         else:
#             dir = pathlib.Path(cls.base_dir)

#             if not dir.is_dir():
#                 raise NoBaseDirExists(cls.base_dir)

#     @classmethod
#     def validate_config(cls):
#         """Test if config files exist and create them if needed"""

#         dir = pathlib.Path(cls.conf_dir)
#         if not dir.is_dir():
#             dir.mkdir(parents=True, exist_ok=True)

#         files = [
#             cls.conf_file,
#             cls.filters_file,
#             cls.library_file,
#         ]

#         for file in files:
#             f = pathlib.Path(file)

#             if not f.is_file():
#                 f.touch()
