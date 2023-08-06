"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This subpackage contains the command line client definiton.
"""

from .main import main
from .profile import profile  # noqa: F401 - We are importing these for Click
from .config import config  # noqa: F401 - We are importing these for Click


if __name__ == '__main__':
    main()
