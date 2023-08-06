"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This subpackage contains the handlers for working with addons, including
their downloading, version checks, and dependency management.
"""

from hashlib import md5
from pathlib import Path
from pydantic import HttpUrl
from typing import Dict, List, Optional
import requests

from ..util import make_logger
from ..config import Config
from ..config.common import BaseModel, Version
from ..exceptions import GithubRateLimitError
from ..game import GuildWars2

logger = make_logger()

extras = [
    {
        'name': 'boontable',
        'dll_suffix': 'table',
        'github_project': 'knoxfighter/GW2-ArcDPS-Boon-Table'
    },
    {
        'name': 'mechanics',
        'dll_suffix': 'mechanics',
        'github_project': 'knoxfighter/GW2-ArcDPS-Mechanics-Log'
    },
    {
        'name': 'killproof',
        'dll_suffix': 'killproof_me',
        'github_project': 'knoxfighter/arcdps-killproof.me-plugin'
    },
    {
        'name': 'healing',
        'dll_prefix': False,
        'dll_suffix': 'healing_stats',
        'github_project': 'Krappa322/arcdps_healing_stats'
    },
]


class GeeWhiz2AddonBase(BaseModel):
    """A class to define the interfaces for addon management."""

    config: Config

    @property
    def destination(self) -> Path:
        """Render the path based on configuration and addon details."""
        if self.config.loaded.arcdps.directx == 'dx9':
            return GuildWars2(config=self.config).gamedir.joinpath('bin64').joinpath(self.filename)
        else:
            return GuildWars2(config=self.config).gamedir.joinpath(self.filename)


class GeeWhiz2AddonArcDPS(GeeWhiz2AddonBase):
    """A class to define ArcDPS management."""

    name: str = 'arcdps'
    url: HttpUrl = 'https://www.deltaconnected.com/arcdps/x64/d3d11.dll'
    sumurl: HttpUrl = 'https://www.deltaconnected.com/arcdps/x64/d3d11.dll.md5sum'
    latest_known_sum: Optional[str]

    @property
    def filename(self) -> str:
        """Return the correct filename depending on DirectX mode."""
        return 'd3d9.dll' if self.config.loaded.arcdps.directx == 'dx9' else 'd3d11.dll'

    @property
    def latest_sum(self) -> str:
        """Return the MD5 digest of the latest release."""
        if self.latest_known_sum is None:
            self.latest_known_sum = requests.get(self.sumurl).text.split()[0]
            logger.debug(f'The latest known MD5 sum is: {self.latest_known_sum}')
        return self.latest_known_sum

    @property
    def current_sum(self) -> Optional[str]:
        """Return the MD5 digest of the existing installation."""
        if self.destination.exists():
            md5_hash = md5(usedforsecurity=False)
            with open(self.destination, 'rb') as f:
                md5_hash.update(f.read())
            logger.debug(f'The MD5 sum of the existing ArcDPS install is: {md5_hash.hexdigest()}')
            return md5_hash.hexdigest()
        return None

    @property
    def needs_update(self) -> bool:
        """Identify if the installed version sum doesn't match the latest sum."""
        if not self.config.loaded.arcdps.update:
            logger.debug('Ignoring update per configuration for ArcDPS')
            return False
        needs_update = self.latest_sum != self.current_sum
        logger.info(f'We do{"" if needs_update else " not"} appear to need to update ArcDPS.')
        return needs_update

    def update(self) -> None:
        """Download the latest release."""
        if self.needs_update:
            logger.info('Downloading newest version of ArcDPS.')
            with self.config.downloader(url=self.url, dest=self.destination) as downloader:
                downloader.show()
            if self.needs_update:  # pragma: nocover (This is an error case we don't expect to hit)
                raise RuntimeError("Newest update doesn't appear to match expected sum.")


class GeeWhiz2AddonArcDPSExtra(GeeWhiz2AddonBase):
    """A class to define ArcDPS Extra management."""

    name: str
    dll_prefix: bool = True
    dll_suffix: str
    github_project: str
    releases: Optional[List[Dict]]
    sanitized_releases: Optional[List[Version]]

    @property
    def filename(self) -> str:
        """Identify the filename for this addon."""
        if self.dll_prefix:
            base = 'd3d9_arcdps' if self.config.loaded.arcdps.directx == 'dx9' else 'd3d11_arcdps'
        else:
            base = 'arcdps'
        return f'{base}_{self.dll_suffix}.dll'

    @property
    def extra_config(self) -> BaseModel:
        """Return the configuration for this extra."""
        return getattr(self.config.loaded.arcdps.extras, self.name)

    def sanitize_releases(self) -> None:
        """Download and sanitize releases using Version."""
        if self.releases is None:
            self.releases = requests.get(f'https://api.github.com/repos/{self.github_project}/releases').json()
            logger.debug(f'Identified releases for {self.name}: {[release["tag_name"] for release in self.releases]}')
        if isinstance(self.releases, dict):  # pragma: nocover (obviously don't count on this)
            logger.error(f'GitHub appears to have rate limited us. Response: {self.releases}')
            raise GithubRateLimitError('GitHub has rate limited our ability to parse releases for {self.name}')
        if self.sanitized_releases is None:
            self.sanitized_releases = [Version(release['tag_name']) for release in self.releases]

    @property
    def latest_github_version(self) -> Optional[Version]:
        """Return the latest version available according to the GitHub API."""
        prerelease_ok = self.extra_config.prerelease

        try:
            self.sanitize_releases()
        except GithubRateLimitError:
            logger.warning(f'Just marking current version as latest: {getattr(self.config.state, self.name)}')
            return getattr(self.config.state, self.name)

        # Find the highest semver in the releases
        latest_version = Version('0.0.0')
        for i, release in enumerate(self.releases):
            release_version = self.sanitized_releases[i]
            if release['prerelease'] and not prerelease_ok:
                continue
            if release_version > latest_version:
                latest_version = release_version

        logger.debug(f'Latest release appears to be: {latest_version}')

        if latest_version == Version('0.0.0'):  # pragma: nocover (This is an error case we hope to not hit)
            raise RuntimeError('Unable to determine version from Github release for {self.name}')

        return latest_version

    @property
    def desired_version(self) -> Optional[Version]:
        """Return the version specified in configuration."""
        return self.extra_config.version

    @property
    def needs_update(self) -> bool:
        """Identify if the installed version is below the latest version."""
        installed_version = getattr(self.config.state, self.name)
        # If the user doesn't want to update, then we never need to
        if not self.extra_config.update:
            logger.debug(f'Ignoring {self.name} update per configuration')
            return False
        # If there is no version installed, we always have to
        if installed_version is None or not self.destination.exists():
            logger.debug(f'Not tracking an installed version of {self.name}')
            return True
        # If the desired version is specified, then we have to update if it doesn't match the installed version
        if self.desired_version is not None:
            return self.desired_version != installed_version
        # If there is a version installed, and no version was pinned in config, then we need to update if we don't have
        # the latest version available on GitHub
        return installed_version != self.latest_github_version

    def update(self) -> None:
        """Update the addon by downloading the latest release."""
        if not self.needs_update:
            return None

        self.sanitize_releases()
        latest_release_version = self.latest_github_version
        # Get the full release object for the latest version
        for release, release_version in zip(self.releases, self.sanitized_releases):
            if release_version == latest_release_version:
                latest_release = release
                break

        # Get the asset object for the .dll file from the latest release
        latest_release_asset = list(filter(
            lambda asset: asset.get('name', '').endswith('.dll'),
            latest_release.get('assets', [])
        ))[0]
        # Get the asset download url from the asset object
        download_url = latest_release_asset.get('browser_download_url', '')
        logger.info(f'Downloading newest version of {self.name} ({latest_release_version})')
        with self.config.downloader(url=download_url, dest=self.destination) as downloader:
            downloader.show()
        logger.debug(f'Noting latest version ({latest_release_version}) in state.')
        setattr(self.config.state, self.name, latest_release_version)
        self.config.state.save()
        logger.debug(self.config.state)
        if self.needs_update:  # pragma: nocover (This is an error case we don't expect to hit)
            raise RuntimeError("Newest update didn't appear to save to state.")
