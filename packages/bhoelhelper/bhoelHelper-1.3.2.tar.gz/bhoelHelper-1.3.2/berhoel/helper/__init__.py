#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Misc helper
"""

# Standard library imports.
import time
from enum import Enum, auto
from datetime import timedelta
from contextlib import contextmanager

try:
    # Local library imports.
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0.invalid0"

__date__ = "2022/07/30 18:29:32 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 1999, 2000, 2021, 2022 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "bhoel@starship.python.net"


class SwirlSelect(Enum):
    LINES = auto()
    DOTS = auto()


__swirl_string = {
    SwirlSelect.LINES: r"\|/-",
    SwirlSelect.DOTS: (
        "\N{BRAILLE PATTERN DOTS-123}"  # "⠇"
        "\N{BRAILLE PATTERN DOTS-237}"  # "⡆"
        "\N{BRAILLE PATTERN DOTS-378}"  # "⣄"
        "\N{BRAILLE PATTERN DOTS-678}"  # "⣠"
        "\N{BRAILLE PATTERN DOTS-568}"  # "⢰"
        "\N{BRAILLE PATTERN DOTS-456}"  # "⠸"
        "\N{BRAILLE PATTERN DOTS-145}"  # "⠙"
        "\N{BRAILLE PATTERN DOTS-124}"  # "⠋"
    ),
}


def swirl(style=SwirlSelect.LINES):
    """Generator to show a swirling life indicator.

    >>> sw = swirl()
    >>> a = [_ for _ in zip(range(5), sw)]
    \\...|.../...-...\\...
    >>> sw = swirl(SwirlSelect.DOTS)
    >>> a = [_ for _ in zip(range(8), sw)]
    ⠇...⡆...⣄...⣠...⢰...⠸...⠙...⠋...

    Returns:
      `generator`: printing running indicator.
    """
    sw_string = __swirl_string[style]
    while True:
        for c in sw_string:
            print(c, end="\r")
            yield


def count_with_msg(msg="loop", start=0):
    """Counting variable with start value and message.

    >>> c = count_with_msg("msg", 5)
    >>> print([i for _, i in zip(range(5),c)] == [5, 6, 7, 8, 9])
    msg 1 ...msg 2 ...msg 3 ...msg 4 ...msg 5 ...True
    >>>

    Args:
        msg (str): base message
        start (int): counter start_time

    Returns:
        `generator`: counter with message.
    """
    i = 1
    _count = start
    while True:
        print("{} {} ".format(msg, i), end="\r")
        yield _count
        _count += 1
        i += 1


@contextmanager
def process_msg_context(msg):
    """Provides a context for calling routines and reporting entering and exit.

    >>> with process_msg_context("do something"):
    ...     pass
    do something......do something...done
    >>>

    Args:
        msg (str): message for bracing process.

    Returns:
        `contextmanager`: bracing message.
    """
    print("{}...".format(msg), end="\r")
    yield
    print("{}...done".format(msg))


@contextmanager
def timed_process_msg_context(msg, time_form=None):
    """Provides a context for calling routines and reporting entering and exit.
    Report spent time.

    >>> with timed_process_msg_context("do something"):
    ...     time.sleep(1)
    do something......do something...done (0:00:01)
    >>> with timed_process_msg_context("do something", lambda t:"{:d}s".format(int(t))):
    ...     time.sleep(1)
    do something......do something...done (1s)
    >>>

    Args:
        msg (str): message for bracing process.
        time_form (func): function formatting druntime.

    Returns:
        `contextmanager`: bracing message.
    """
    if time_form is None:
        time_form = lambda t: timedelta(seconds=int(t))
    start_time = time.time()
    print("{}...".format(msg), end="\r")
    yield
    print(("{}...done ({})").format(msg, time_form(time.time() - start_time)))


# Local Variables:
# mode: python
# compile-command: "python ../../setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
