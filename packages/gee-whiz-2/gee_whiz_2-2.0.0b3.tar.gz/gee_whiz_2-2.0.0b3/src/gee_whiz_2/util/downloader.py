"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the utility functions for downloading files.
"""

import requests
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Union


from .logger import make_logger
from .tui import console, theme
from ..exceptions import DownloadFailed


class GeeWhiz2BaseDownloader(object):
    """Base class for downloaders, both GUI and TUI."""

    def __init__(self, url: str, dest: Union[Path, str], block_size: int = 1024):
        """Initialize the downloader with persistent information."""
        if not isinstance(dest, Path):
            dest = Path(dest)
        self.logger = make_logger()
        self.url = url
        self.dest = dest
        self.filename = dest.parts[-1]
        self.block_size = block_size

    def __enter__(self) -> 'GeeWhiz2BaseDownloader':
        """Context manager enter for the downloader."""
        self.logger.info(f'Downloading from {self.url}.')
        self.tf = NamedTemporaryFile()
        self.response = requests.get(self.url, stream=True)
        self.size = int(
            self.response.headers.get('content-length', 0)
        ) or int(
            self.response.headers.get('Content-Length', 0)
        ) or 0
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit for the downloader."""
        # Copy the temporary file to the destination
        self.dest.parent.mkdir(exist_ok=True, parents=True)
        self.logger.info(f'Writing {self.filename} to {self.dest}')
        with open(self.dest, 'wb') as df:
            self.tf.seek(0)
            df.write(self.tf.read())
        self.tf.close()

    def show(self):
        """Show the download progress (implemented by subclasses)."""
        raise NotImplementedError("Specify either a GUI or TUI downloader.")


class GeeWhiz2TuiDownloader(GeeWhiz2BaseDownloader):
    """Downloader with a TUI progress bar."""

    def show(self):
        """Show the download progress (with a TUI progress bar)."""
        from rich.progress import (
            BarColumn,
            DownloadColumn,
            Progress,
            TextColumn,
            TimeRemainingColumn,
            TransferSpeedColumn,
        )
        progress = Progress(
            TextColumn(f"[{theme.blue}]{{task.fields[filename]}}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
            console=console
        )
        task = progress.add_task("download", filename=self.filename)
        progress.update(task, total=self.size)
        with progress:
            for data in self.response.iter_content(self.block_size):
                self.tf.write(data)
                progress.update(task, advance=len(data))
        if self.size != 0 and progress.tasks[0].completed != self.size:
            raise DownloadFailed('Something about the download failed as the written bytes were the wrong size.')


class GeeWhiz2GuiDownloader(GeeWhiz2BaseDownloader):
    """Downloader with a GUI popup."""

    _tui_download = GeeWhiz2TuiDownloader.show

    def show(self):
        """Show the download progress (with a GUI popup)."""
        self.logger.warning('GUI interfaces have not been implemented yet.')
        self._tui_download()
