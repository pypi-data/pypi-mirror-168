"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the utility functions for logging configuration.
"""

import logging
import logging.handlers
from pathlib import Path
from rich.logging import RichHandler


def make_logger(verbosity: int = None):
    """Make a consistent logger that respects persistent verbosity settings."""
    logger = logging.getLogger('gw2')
    logger.setLevel(logging.DEBUG)

    if len(logger.handlers) != 2 or (not Path('/dev/log').exists() and len(logging.handlers) != 1):
        formatter = logging.Formatter('%(message)s')

        stderr = RichHandler(rich_tracebacks=True)
        stderr.setFormatter(formatter)
        if verbosity is not None:
            stderr.setLevel(40 - (min(3, verbosity) * 10))
        else:
            stderr.setLevel(40)
        logger.addHandler(stderr)

        if Path('/dev/log').exists():
            syslog = logging.handlers.SysLogHandler(address='/dev/log')
            syslog.setFormatter(formatter)
            syslog.setLevel(logging.INFO)
            logger.addHandler(syslog)
    else:
        if verbosity is not None:
            stderr = logger.handlers[0]
            # Never lower the verbosity after it's been made high
            stderr.setLevel(min(stderr.level, 40 - (min(3, verbosity) * 10)))

    return logger
