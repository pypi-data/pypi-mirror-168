"""
    The MIT License (MIT)

    © 2016 Allon Hadaya <self@allon.nyc>

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""
import re
import subprocess


class DmenuError(Exception):
    """The base class for dmenu errors."""

    pass


class DmenuCommandError(DmenuError):
    """The dmenu command failed."""

    def __init__(self, args, error):
        super(DmenuCommandError, self).__init__(
            "The provided dmenu command could not be used (%s): %s" % (args, error)
        )


class DmenuUsageError(DmenuError):
    """The dmenu command does not support your usage."""

    def __init__(self, args, usage):
        super(DmenuUsageError, self).__init__(
            "This version of dmenu does not support your usage (%s):\n\n%s"
            % (args, usage)
        )


def version(command="dmenu"):
    """The dmenu command's version message.

    Raises:
        DmenuCommandError

    Example:

        >>> import dmenu
        >>> dmenu.version()
        'dmenu-4.5, \xc2\xa9 2006-2012 dmenu engineers, see LICENSE for details'
    """

    args = [command, "-v"]

    try:
        # start the dmenu process
        proc = subprocess.Popen(
            args,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as err:
        # something went wrong with starting the process
        raise DmenuCommandError(args, err)

    if proc.wait() == 0:
        # version information from stdout
        return proc.stdout.read().rstrip("\n")

    # error from dmenu
    raise DmenuCommandError(args, proc.stderr.read())


def show(
    items,
    command="dmenu",
    command_args=[],
    case_insensitive=None,
    lines=None,
    monitor=None,
    prompt=None,
):
    """Present a dmenu to the user.

    Args:
        items (Iterable[str]):
            defines the menu items being presented to the user. items should
            not contain the newline character.

        command (Optional[str]):
            defines the path to the dmenu executable. Defaults to 'dmenu'.

        command_args (Iterable[str]):
            generic way to add arguments to 'command', e.g. to use
            command="rofi" and command_args=["-dmenu"]

        case_insensitive (Optional[bool]):
            dmenu matches menu items case insensitively.

        lines (Optional[int]):
            dmenu lists items vertically, with the given number of lines.

        monitor (Optional[int]):
            dmenu is displayed on the monitor number supplied. Monitor numbers
            are starting from 0.

        prompt (Optional[str]):
            defines the prompt to be displayed to the left of the input field.

    Raises:
        DmenuCommandError
        DmenuUsageError

    Returns:
        The user's selected menu item, their own typed item, or None if they hit escape.

    Examples:

        >>> import dmenu

        >>> dmenu.show(['a', 'b', 'c'])
        'a'  # user selected a

        >>> dmenu.show(['a', 'b', 'c'], prompt='pick a letter')
        'b'  # user selected b

        >>> dmenu.show(['a', 'b', 'c'])
        None  # user hit escape

        >>> dmenu.show(['a', 'b', 'c'])
        'd'  # user typed their own selection, d

        >>> dmenu.show(['a', 'b', 'c'], command='not_a_valid_dmenu')
        Traceback (most recent call last):
          ...
        dmenu.dmenu.DmenuCommandError: The provided dmenu command could not be used (['not_a_valid_dmenu']): [Errno 2] No such file or directory: 'not_a_valid_dmenu'

        >>> dmenu.show(['a', 'b', 'c'], monitor=2)
        Traceback (most recent call last):
          ...
        dmenu.dmenu.DmenuUsageError: This version of dmenu does not support your usage (['dmenu', '-m', '2']):
        usage: dmenu [-b] [-f] [-i] [-l lines] [-p prompt] [-fn font]
                     [-nb color] [-nf color] [-sb color] [-sf color] [-v]

        Consider configuring show using partial application:

        >>> import functools
        >>> show = functools.partial(dmenu.show, bottom=True)
        >>> show(['we', 'show', 'up', 'below'])
        >>> show(['us', 'too'])
    """

    # construct args

    args = [command] + command_args

    if case_insensitive:
        args.append("-i")

    if lines is not None:
        args.extend(("-l", str(lines)))

    if monitor is not None:
        args.extend(("-m", str(monitor)))

    if prompt is not None:
        args.extend(("-p", prompt))

    try:
        # start the dmenu process
        proc = subprocess.Popen(
            args,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as err:
        # something went wrong with starting the process
        raise DmenuCommandError(args, err)

    # write items over to dmenu
    with proc.stdin:
        for item in items:
            proc.stdin.write(item)
            proc.stdin.write("\n")

    if proc.wait() == 0:
        # user made a selection
        return proc.stdout.read().rstrip("\n")

    stderr = proc.stderr.read()

    if stderr == "":
        # user hit escape
        return None

    if re.match("usage", stderr, re.I):
        # usage error
        raise DmenuUsageError(args, stderr)

    # other error from dmenu
    raise DmenuCommandError(args, stderr)
