"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This subpackage contains the necessary classes to manage Guild Wars 2 Local.dat
profiles, including the account/passwords saved in those profiles.
"""

from typing import Optional, Union

from ..config import Config
from ..exceptions import GuildWars2ProfileNotAvailable
from ..util import make_logger
logger = make_logger()

from .profiles import GuildWars2Profile


class GuildWars2Profiles(object):
    """GuildWars2Profiles - a class to track the set of all managed profiles."""

    def __init__(self, config: Config = None):
        """Intialize tracking of profiles."""
        if config is None:
            config = Config()
        self.config = config
        self.profiles = set()
        for profile_name in config.state.profiles.available:
            self.profiles.add(GuildWars2Profile(name=profile_name, config=config))

    def __iter__(self):
        """Iterate over the profiles included."""
        yield from sorted(self.profiles)

    @property
    def current(self):
        """Return the currently configured profile."""
        return self.config.state.profiles.current

    def add(self, profile_name: str = None):
        """Add a profile to the set of managed profiles."""
        profile = GuildWars2Profile(name=profile_name, config=self.config)
        if not profile.storage_exists:
            profile.create_storage()
        self.profiles.add(profile)
        self._update_state()

    def rm(self, profile_name: str = None):
        """Remove a profile from the set of managed profiles."""
        profile = GuildWars2Profile(name=profile_name, config=self.config)
        try:
            self.profiles.remove(profile)
            self._update_state()
        except KeyError:
            logger.warning(f'Attempt was made to remove untracked profile, {profile_name}. Continuing...')
        profile.rm()

    def set(self, profile_name: Optional[Union[str, GuildWars2Profile]] = None):
        """Set a given profile from those available as the current profile."""
        profile = GuildWars2Profile(name=profile_name, config=self.config)
        if self.current is not None:
            current_profile = GuildWars2Profile(name=self.current, config=self.config)
        else:
            current_profile = None
        if profile in self.profiles and not profile == current_profile:
            profile.swap_for(current_profile)
            self._update_state()
        elif profile == current_profile:
            logger.info(f'{profile_name} is already set as the current profile.')
        else:
            raise GuildWars2ProfileNotAvailable(f"Unable to set {profile_name} as current profile as it's unavailable.")

    def _update_state(self):
        """Update the state yaml with the current state of profile management."""
        self.config.state.profiles.available = [str(profile) for profile in self.profiles]
        self.config.state.save()


__all__ = [GuildWars2Profiles, GuildWars2Profile]
