#!/usr/bin/env python3
from .dmenu import show as dmenu_show
from .dmenu import (
    DmenuCommandError,
    DmenuUsageError,
    DmenuError
)
from .fzf import FzfPrompt


class InvalidCmdPrompt(Exception):
    '''Exception raised when user has invalid command prompt'''

    def __init__(self, error,  message='ERROR: prompt_cmd not recognized'):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} "{self.error}"'


class InputError(Exception):
    '''Exception fzf or dmenu prompt fails'''

    def __init__(self, error,  message='ERROR: Could not get user input',
                 prefix=''):
        self.error = error
        self.prefix = prefix
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.prefix}{self.message}{self.error}'


def dmenu_prompt(
        items,
        command='dmenu',
        command_args=[],
        case_insensitive=None,
        lines=None,
        monitor=None,
        prompt=None):

    choice = None
    try:
        choice = dmenu_show(
            items=items,
            command=command,
            command_args=command_args,
            case_insensitive=case_insensitive,
            lines=lines,
            monitor=monitor,
            prompt=prompt)

    except (DmenuCommandError, DmenuUsageError, DmenuError) as err:
        raise InputError(err)

    except KeyboardInterrupt:
        raise InputError('User interruption...stopping', message='')

    return choice


def fzf_auto(options, prompt):
    choice = None
    try:
        print(f'Auto title: {options[0]}')
        choice = input(prompt)
        if choice == '':
            choice = options[0]

    except KeyboardInterrupt:
        raise InputError('User interruption...stopping',
                         message='',  prefix='\n')

    return choice


def fzf_prompt(options, prompt):
    choice = None
    try:
        fzf = FzfPrompt()
        choice = fzf.prompt(options, f'--prompt="{prompt}"')

    except SystemError as err:
        raise InputError(err)

    return choice


def user_choice(options, user, prompt,
                other_message=None, other_position='last',
                auto_title=False):
    '''Give user a prompt to choose from a list of options.
       Uses dmenu, fzf, or rofi'''
    cmd = user.prompt_cmd
    if cmd == 'dmenu':
        choice = dmenu_prompt(options, command=cmd, prompt=prompt,
                              lines=20, case_insensitive=True)

    elif cmd == 'rofi':
        choice = dmenu_prompt(options, command=cmd, prompt=prompt,
                              command_args=['-dmenu'])

    elif cmd == 'fzf':
        if auto_title:
            choice = fzf_auto(options, prompt)

        else:
            choice = fzf_prompt(options, prompt)
            if len(choice) == 1:
                choice = choice[0]

    else:
        raise InvalidCmdPrompt(user.prompt_cmd)

    return choice
