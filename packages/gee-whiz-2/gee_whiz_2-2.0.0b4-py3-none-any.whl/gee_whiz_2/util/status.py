"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the utility functions for showing work being done.
"""

from .logger import make_logger
from .tui import console


class GeeWhiz2BaseStatus(object):
    """Base class for status busy display, both GUI and TUI."""

    def __init__(self, text: str = None):
        """Initialize the status with text."""
        self.logger = make_logger()
        self.text = text

    @property
    def indicator(self):
        """Show the busy status (implemented by subclasses)."""
        raise NotImplementedError("Specify either a GUI or TUI status.")


class GeeWhiz2TuiStatus(GeeWhiz2BaseStatus):
    """Status busy display for the TUI."""

    @property
    def indicator(self):
        """Return the object with a context manager to show busy status in the TUI."""
        return console.status(f'{self.text}...')


class GeeWhiz2GuiStatus(GeeWhiz2BaseStatus):
    """Status busy display for the GUI."""

    _tui_indicator = GeeWhiz2TuiStatus.indicator

    @property
    def indicator(self):
        """Return the object with a context manager to show busy status in the GUI."""
        self.logger.warning("GUI interfaces have not been implemented yet.")
        self._tui_indicator
