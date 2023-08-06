"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the utility functions for downloading files.
"""

from rich.console import Console
from rich.theme import Theme


# Save our themes to get some consistency in Rich
class GW2Theme(object):
    """A simple theme dataclass/object to save theme settings."""

    pygment: str = 'github-dark'
    fg: str = '#c9d1d9'
    subtle: str = '#6e7681'
    bg: str = '#0d1117'
    red: str = '#ff7b72'
    bright_red: str = '#ffa198'
    blue: str = '#79c0ff'
    bright_blue: str = '#a5d6ff'
    green: str = '#56d364'
    bright_green: str = '#7ee787'


theme = GW2Theme()
rich_theme = Theme({
    'repr.number': theme.fg,
    'repr.number_complex': theme.fg,
    'repr.path': theme.blue,
    'repr.filename': theme.bright_blue,
    'progress.data.speed': theme.subtle,
    'progress.download': theme.green,
    'progress.percentage': theme.blue,
    'progress.remaining': theme.red,
    'bar.back': theme.bg,
    'bar.complete': theme.green,
    'bar.finished': theme.bright_green
})

console = Console(theme=rich_theme)
