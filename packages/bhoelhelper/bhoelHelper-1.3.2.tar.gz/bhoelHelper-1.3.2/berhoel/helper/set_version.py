#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Set lib version from `pyproject.toml`.

This library allows for setting the version number for a library from
the pyproject.toml file.

Add to your `pyproject.toml` add a new section:

.. code-block:: toml

  [tool.berhoel.helper.set_version]
  version_files = ["berhoel/helper/_version.py"]

Generate the version file:

.. code-block:: shell

  > poetry run set_lib_version
  writing berhoel/helper/_version.py

In the library `__init__.py` just use:

.. code-block:: python

  try:
      from ._version import __version__
  except ImportError:
      __version__ = "0.0.0.invalid0"
"""

# Standard library imports.
import argparse
from pathlib import Path

# Third party library imports.
import tomli

# Local library imports.
from . import __version__

__date__ = "2022/09/24 13:01:39 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020, 2022 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


def build_parser():
    "Build cli parser."
    parser = argparse.ArgumentParser(
        prog="set_lib_version",
        description="Create version files with version number from `pyproject.toml`.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser


def build():
    """Create version files with version number from `pyproject.toml`."""

    parser = build_parser()
    parser.parse_args()

    PYPROJECT = (Path() / "pyproject.toml").resolve()

    with PYPROJECT.open("rb") as conf_inp:
        CONFIG = tomli.load(conf_inp)

    VERSION = CONFIG["tool"]["poetry"]["version"]
    VER_FILES = CONFIG["tool"]["berhoel"]["helper"]["set_version"]["version_files"]
    for ver_file in VER_FILES:
        print(f"writing {ver_file!s}")
        with Path(ver_file).resolve().open("w") as target:
            target.write(f'__version__ = "{VERSION}"\n')


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "50/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
