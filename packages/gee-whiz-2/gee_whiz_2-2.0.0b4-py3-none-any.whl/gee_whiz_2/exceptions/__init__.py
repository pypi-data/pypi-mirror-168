"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains common exceptions.
"""


class ConfigVersionNotPresent(Exception):
    """Exception raised when a config file is presented with no version defined.

    Attributes:
        yaml_file -- the path to the config file
        message -- explanation of the error
    """

    def __init__(self, yaml_file: str = None, message: str = None):
        """Construct the message using the proper attributes."""
        if message is None:
            if yaml_file is not None:
                message = (
                    f'"config_version" field undefined in {yaml_file}'
                )
            else:
                message = '"config_version" field undefined'
        self.yaml_file = yaml_file
        self.message = message
        super().__init__(self.message)


class ConfigVersionInvalid(Exception):
    """Exception raised when a config file is presented with an invalid version.

    Attributes:
        provided -- the provided version in the config file
        yaml_file -- the path to the config file
        message -- explanation of the error
    """

    def __init__(self, provided: str = None, yaml_file: str = None,
                 valid_versions: str = None, message: str = None):
        """Construct the message using the proper attributes."""
        if message is None:
            if yaml_file is not None:
                message = (
                    f'"config_version" in {yaml_file} is not a valid version'
                )
            else:
                message = '"config_version" is not a valid version'
            if valid_versions is not None:
                message += f' (one of [{valid_versions}])'
        self.provided = provided
        self.yaml_file = yaml_file
        self.message = message
        super().__init__(self.message)


class DownloadFailed(Exception):
    """Exception raised when a download appears to have downloaded the wrong data."""

    pass


class GithubRateLimitError(Exception):
    """Exception raised when GitHub appears to have rate-limited out API calls."""

    pass


class SteamGuildWars2NotFound(Exception):
    """Exception raised when unable to find Guild Wars 2 in the Steam registry."""

    pass


class LutrisNotInstalled(Exception):
    """Exception raised when unable to import Lutris from the system python packages."""

    pass


class LutrisGuildWars2NotFound(Exception):
    """Exception raised when unable to find Guild Wars 2 as a Lutris game."""

    pass


class GW2ProfileAlreadyInstalled(Exception):
    """Exception raised when a profile installation action would overwrite an existing profile."""

    pass


class OtherGW2ProfileInstalled(Exception):
    """Exception raised when some other profile is installed and we expected it to not be."""

    pass


class GuildWars2ProfileNotAvailable(Exception):
    """Exception raised when a profile operated on in a way that requires that it be available, and it's not."""

    pass
