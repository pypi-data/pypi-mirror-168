"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the utility functions for picking a set of options.
"""

from typing import List

from .logger import make_logger
from .tui import console


class GeeWhiz2BasePicker(object):
    """Base class for pickers, both GUI and TUI."""

    def __init__(self, options: List[str], current: str = None):
        """Initialize the picker with options."""
        self.logger = make_logger()
        self.options = options
        self.current = current

    def choose(self):
        """Show the picker (implemented by subclasses)."""
        raise NotImplementedError("Specify either a GUI or TUI picker.")


class GeeWhiz2TuiPicker(GeeWhiz2BasePicker):
    """Picker for the TUI."""

    def choose(self) -> str:
        """Show the picker TUI, return the choice."""
        from rich.prompt import Prompt
        return Prompt.ask(
            prompt='Select the profile to use',
            console=console,
            choices=self.options,
            default=self.current
        )


class GeeWhiz2GuiPicker(GeeWhiz2BasePicker):
    """Picker for the GUI."""

    _tui_choose = GeeWhiz2TuiPicker.choose

    def choose(self) -> str:
        """Show the picker GUI, return the choice."""
        self.logger.warning("GUI interfaces have not been implemented yet.")
        self._tui_choose()
