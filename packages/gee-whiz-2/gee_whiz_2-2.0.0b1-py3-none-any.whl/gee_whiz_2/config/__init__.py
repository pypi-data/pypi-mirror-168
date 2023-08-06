"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This subpackage contains the configuration file models for validating
the types of configuration entries.
"""


from itertools import product
from pathlib import Path
import os
from typing import Optional, Tuple
import yaml
from ..exceptions import ConfigVersionInvalid, ConfigVersionNotPresent
from .common import BaseModel, Version, GeeWhiz2State
from .config_0_1_0 import GeeWhiz2Config as GeeWhiz2Config_0_1_0
from ..util import (
    GeeWhiz2TuiDownloader,
    GeeWhiz2GuiDownloader,
    GeeWhiz2TuiPicker,
    GeeWhiz2GuiPicker,
    GeeWhiz2TuiStatus,
    GeeWhiz2GuiStatus,
    make_logger
)

logger = make_logger()

GEE_WHIZ_2_CONFIG_VERSIONS = {
    '0.1.0': GeeWhiz2Config_0_1_0
}

GEE_WHIZ_2_CONFIG_DIRS = [
    Path(os.environ.get('HOME', '/home/fake')).joinpath('.config/gw2'),
    Path('/etc/gw2')
]

GEE_WHIZ_2_CONFIG_FILES = [
    'config.yml',
    'config.yaml'
]

GEE_WHIZ_2_CONFIG_PATHS = [
    config_dir.joinpath(config_file)
    for config_dir, config_file in product(GEE_WHIZ_2_CONFIG_DIRS, GEE_WHIZ_2_CONFIG_FILES)
]


class Config(object):
    """Config - a high-level wrapper to abstract configuration and state context."""

    def __init__(self, config_path: Path = None) -> None:
        """Initialize a Config object, optionally with a specified path."""
        if config_path is None:
            logger.debug('No config path provided, autoloading')
            autoloaded_config_path, autoloaded_config = self._autoload_config()
            if autoloaded_config is None:
                config_version, config_model = list(GEE_WHIZ_2_CONFIG_VERSIONS.items())[-1]
                logger.info(f'No automatic config identified, loading default config version {config_version}')
                self.loaded_from = None
                self.loaded = config_model(config_version=config_version)
            else:
                logger.debug(f'Config loaded successfully, version {autoloaded_config.config_version}')
                self.loaded_from = autoloaded_config_path
                self.loaded = autoloaded_config
        else:
            logger.debug(f'Specific config path requested: {config_path}')
            self.load_config(config_path)
        self.state = GeeWhiz2State.load()
        logger.debug(f'Initialized config: {self.loaded.dict()}')
        logger.debug(f'Initialized state: {self.state.dict()}')

    def load_config(self, config_path: Path) -> None:
        """Load the passed config path, save it to the loaded attribute."""
        if not isinstance(config_path, Path):
            config_path = Path(config_path)
        logger.info(f'Loading requested config at {config_path}')
        self.loaded_from = config_path
        self.loaded = self._load_config(config_path)
        logger.debug(f'Loaded config: {self.loaded.dict()}')

    @property
    def downloader(self):
        """Return the correct downloader for the loaded configuration."""
        logger.debug(f'Returning downloader for {self.loaded.interface}')
        if self.loaded.interface == 'tui':
            return GeeWhiz2TuiDownloader
        elif self.loaded.interface == 'gui':
            return GeeWhiz2GuiDownloader
        else:
            raise NotImplementedError(f'Unable to set a downloader for interface of type {self.loaded.interface}')

    @property
    def picker(self):
        """Return the correct picker for the loaded configuration."""
        logger.debug(f'Returning picker for {self.loaded.interface}')
        if self.loaded.interface == 'tui':
            return GeeWhiz2TuiPicker
        elif self.loaded.interface == 'gui':
            return GeeWhiz2GuiPicker
        else:
            raise NotImplementedError(f'Unable to set a picker for interface of type {self.loaded.interface}')

    @property
    def status(self):
        """Return the correct status indicator for the loaded configuration."""
        logger.debug(f'Returning status for {self.loaded.interface}')
        if self.loaded.interface == 'tui':
            return GeeWhiz2TuiStatus
        elif self.loaded.interface == 'gui':
            return GeeWhiz2GuiStatus
        else:
            raise NotImplementedError(f'Unable to set a picker for interface of type {self.loaded.interface}')

    @staticmethod
    def _load_config(yaml_file: Path) -> BaseModel:
        """Instantiate a configuration of the right version from a file."""
        with open(yaml_file) as f:
            config = yaml.safe_load(f)
        logger.debug(f'Config file content: {config}')
        config_version = config.get('config_version')
        if config_version is None:
            raise ConfigVersionNotPresent(yaml_file)
        config_version = str(Version(config_version))
        logger.debug(f'Identified config version to be loaded: {config_version}')
        config_model = GEE_WHIZ_2_CONFIG_VERSIONS.get(config_version)
        if config_model is None:
            valid_versions = ', '.join(
                list(GEE_WHIZ_2_CONFIG_VERSIONS.keys())
            )
            raise ConfigVersionInvalid(config_version, yaml_file, valid_versions)
        return config_model.parse_obj(config)

    @classmethod
    def _autoload_config(cls) -> Tuple[Optional[Path], Optional[BaseModel]]:
        """Look through the default config locations and return the first one identified."""
        environ_config = os.environ.get('GW2_CONFIG')
        if environ_config is not None:
            logger.info(f'Loading config from environment: {environ_config}')
            return (environ_config, cls._load_config(yaml_file=Path(environ_config)))
        for possible_path in GEE_WHIZ_2_CONFIG_PATHS:
            logger.debug(f'Looking for config in: {possible_path}')
            if possible_path.exists():
                logger.info(f'Identified config in path: {possible_path}')
                return (possible_path, cls._load_config(yaml_file=possible_path))
        return (None, None)
