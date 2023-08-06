"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the code for managing Guild Wars 2 Profiles (the Local.dat
file) with the ability to create new named profiles, change the active profile
for a given Guild Wars 2 installation, and remove profiles and their
recorded states.
"""

import shutil

from ..config import Config, GEE_WHIZ_2_CONFIG_DIRS
from ..exceptions import GW2ProfileAlreadyInstalled, OtherGW2ProfileInstalled
from ..game import GuildWars2
from ..util import make_logger
logger = make_logger()


class GuildWars2Profile(object):
    """GuildWars2Profile - a class to track the state of a named profile."""

    def __init__(self, name: str = None, config: Config = None):
        """Initialize a GuildWars2Profile object."""
        if config is None:
            config = Config()
        if isinstance(name, self.__class__):
            self.name = name.name
        else:
            self.name = name
        self.config = config
        self.datdir = GuildWars2(config=config).datdir
        logger.debug(f'{repr(self)}.datdir: {self.datdir}')
        logger.debug(f'{repr(self)}.storage_path: {self.storage_path}')

    def __eq__(self, other):
        """Compare a profile to another (or a string, matching the name)."""
        if isinstance(other, type(self)):
            return self.storage_path == other.storage_path
        elif isinstance(other, str):
            return self.name == other
        return False

    def __lt__(self, other):
        """Compare a profile to another (or a string, matching the name) to sort alphabetically."""
        return str(self) < str(other)

    def __hash__(self):
        """Define the unique hash of a profile based on its storage path."""
        return hash(self.storage_path)

    def __str__(self):
        """Return the string representation of a profile as its name."""
        # Path is inferred from the config, so keeping profile names as the mechanism by which
        #   we use string representations for profiles lets us coerce into easy state tracking
        #   (which is also related to the path of the config).
        return self.name

    def __serialize__(self):
        """Return a serializable version of the profile (its String representation)."""
        return str(self)

    @property
    def storage_dir(self):
        """Render the directory to which a profile should be stored when not in use."""
        return getattr(self.config.loaded_from, "parent") or GEE_WHIZ_2_CONFIG_DIRS[0]

    @property
    def storage_path(self):
        """Render the path where a Local.dat file should be saved when not in use."""
        return self.storage_dir.joinpath(self.name).with_suffix('.dat')

    @property
    def storage_exists(self):
        """Return whether or not the existing storage .dat exists."""
        return self.storage_path.exists()

    @property
    def install_path(self):
        """Render the path to which Local.dat should be installed."""
        return self.datdir.joinpath('Local.dat')

    @property
    def install_exists(self):
        """Return whether an installation exists at the install path."""
        exists = self.install_path.exists()
        logger.debug((f'{repr(self)}.install_path: {self.install_path} '
                      f'({"exists" if exists else "does not exist"})'))
        return exists

    @property
    def configured_current(self):
        """Return whether the profile object is the current set in state."""
        current = getattr(self.config.state.profiles, "current") == self.name
        logger.debug(f'{repr(self)}.configured_current: {current}')
        return current

    @property
    def installed(self):
        """Return whether or not the current profile is installed."""
        return self.configured_current and self.install_exists

    def _set_state(self, profile_name: str = None):
        """Set and save the state of the profile configuration."""
        logger.debug(f'Setting state current profile to {profile_name}')
        self.config.state.profiles.current = profile_name
        self.config.state.save()

    def install(self):
        """Copy the stored Local.dat to the installation path, if one doesn't already exist."""
        if not self.installed:  # either we are not configured or no install exists
            # Prevent overwriting existing profile
            if self.install_path.exists():
                raise GW2ProfileAlreadyInstalled('Attempted to install a profile, but another appears to be installed.')
            try:
                logger.debug(f'Copying {self.storage_path} to {self.install_path}')
                shutil.copy2(self.storage_path, self.install_path)
            except FileNotFoundError:
                logger.warning(f'No Local.dat exists for {self.name}. Creating new from existing.')
                self.create_storage()
            self._set_state(self.name)

    def uninstall(self):
        """Move the updated, installed Local.dat to the storage path."""
        if self.installed:
            try:
                logger.debug(f'Moving {self.install_path} to {self.storage_path}')
                shutil.move(self.install_path, self.storage_path)
            except FileNotFoundError:
                logger.warning((f'Attempted to uninstall {self.name} but either: '
                                f'no file existed at {self.install_path} or '
                                f'no directory existed at {self.storage_dir}'))
            self._set_state(None)
        elif not self.install_exists:
            self._set_state(None)
        else:
            raise OtherGW2ProfileInstalled('Attempted to uninstall a profile that is not installed.')

    def create_storage(self):
        """Create a copy of the Local.dat in the storage path."""
        if not self.storage_exists and self.install_exists:
            logger.info(f'Creating new profile storage for {self.name}.')
            shutil.copy2(self.install_path, self.storage_path)
        elif not self.storage_exists:
            logger.warning(f'No profile exists for {self.name} and no base Local.dat to copy.')

    def swap_for(self, other: 'GuildWars2Profile'):
        """Swap this profile for another one by uninstalling the other and installing this one."""
        # If the other profile is insalled, uninstall it and install this one
        if getattr(other, 'installed', None):
            other.uninstall()
            self.install()
        # The only other conditions are:
            # - this profile is installed (install will pass)
            # - some other profile is installed (will raise to prevent overwrite)
            # - no profile is installed (will install this profile)
        else:
            if getattr(self.config.state.profiles, "current") is None and self.install_exists:
                self._set_state(self.name)
            else:
                self.install()

    def rm(self):
        """Remove the profile storage."""
        if self.installed:
            logger.debug('Uninstalling {self.name} profile')
            self.uninstall()
        if self.storage_exists:
            self.storage_path.unlink()
