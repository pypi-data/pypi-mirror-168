"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the code for trying to safely abstract Lutris and Steam
game objects to give us just the information we need from them and let us
cleanly handle starting them through the same methods, while also providing
information from the underlying system about where the game is installed.
"""

from pathlib import Path
import os
import shutil
import sys

from ..config import Config
from ..exceptions import LutrisNotInstalled, LutrisGuildWars2NotFound, SteamGuildWars2NotFound
from ..util import make_logger
logger = make_logger()


class GuildWars2(object):
    """GuildWars2 - a wrapper for the Lutris and Steam Game objects."""

    def __init__(self, config: Config = None):
        """Initialize the Guild Wars 2 object from the loaded configuration."""
        if config is None:
            config = Config()
        if config.loaded.game.type == 'lutris':
            self.game = self.LutrisGuildWars2(config=config)
        elif config.loaded.game.type == 'steam':
            self.game = self.SteamGuildWars2(config=config)
        elif config.loaded.game.type == 'none':
            self.game = self.NullGuildWars2(config=config)
        else:
            raise NotImplementedError(f'No handler is designed to identify games of type {config.loaded.game.type}')
        self.config = config

    def start(self):
        """Wrap the game implementation for start."""
        return self.game.start()

    @property
    def gamedir(self):
        """Wrap the game implementation for gamedir."""
        config_gamedir = self.config.loaded.game.gamedir
        if config_gamedir is None:
            # Let the game implementation find the game
            return self.game.gamedir
        # Return the hard-coded gamedir
        return config_gamedir

    @property
    def datdir(self):
        """Wrap the game implementation for datdir."""
        config_datdir = self.config.loaded.game.datdir
        if config_datdir is None:
            # Let the game implementation find Local.dat
            return self.game.datdir
        # Return the hard-coded datdir
        return config_datdir

    class NullGuildWars2(object):
        """Sets the start function and gamedir property as non-existant."""

        def __init__(self, config: Config):
            """Initialize an empty game object."""
            pass

        def start(self):
            """Unable to start a null game."""
            raise NotImplementedError('Unable to start the game with game type of "none."')

        @property
        def gamedir(self):
            """Unable to identify a gamedir from no game."""
            raise NotImplementedError(
                'Unable to identify the gamedir with game type of "none" and no gamedir set in config.'
            )

        @property
        def datdir(self):
            """Unable to identify a datdir from no game."""
            raise NotImplementedError(
                'Unable to identify the datdir with game type of "none" and no datdir set in config.'
            )

    class LutrisGuildWars2(object):
        """Sets the start function and gamedir property from the Lutris configuration."""

        def __init__(self, config: Config):
            """Initialize a Lutris game from the configured Lutris ID."""
            try:
                import gi
                # Required to import Lutris, as the GObject references require it
                gi.require_version('Gtk', '3.0')

                # Lazyloaded imports let us keep Lutris out of this if we're on steam
                from lutris.game import Game as LutrisGame
                from lutris.game.games_db import get_games
                from lutris.runner_interpreter import get_launch_parameters
                from lutris.util.log import logger as lutris_logger
                self.get_games = get_games
                self.lutris_installed = True
                self.logger = lutris_logger
                self.logger.setLevel(5)
                self.get_launch_parameters = get_launch_parameters

                try:
                    # If no config item was set, we can look for it in the games db
                    lutris_id = config.loaded.game.lutris.id or self.find_lutris_id()
                    # Just set it to something so we get a fake LutrisGame
                    self.lutris_game = LutrisGame(lutris_id)
                    # If the config item is set to a non-existent or the wrong id, we could have a blank name
                    if self.lutris_game.name == '':
                        self.installed = False
                    # If it was set correctly or auto-detected, then we're good
                    elif self.lutris_game.name == "Guild Wars 2":
                        self.installed = True
                    # If it was set to a Lutris ID that exists, but isn't named Guild Wars 2, it's likely wrong.
                    # Still, it was set, so let's just throw a warning and roll with it.
                    else:
                        logger.warning((f"It would appear that Lutris game ID {config.loaded.game.lutris.id} "
                                        f"is not Guild Wars 2, found '{self.lutris_game.name}'"))
                        self.installed = True
                # If the autodetect fails, we know it's not installed
                except LutrisGuildWars2NotFound:
                    logger.error("Auto-detection of Guild Wars 2 installation in Lutris failed.")
                    self.installed = False

            # If Lutris can't be imported, we just basically give up.
            except ModuleNotFoundError:
                logger.error("Lutris is not installed, will be unable to start.")
                self.lutris_installed = False
                self.installed = False
                self.logger = logger

        def find_lutris_id(self):
            """Identify a Lutris game ID for a game named Guild Wars 2."""
            for lutris_game in self.get_games():
                if lutris_game.get('name') == 'Guild Wars 2':
                    return lutris_game.get('id')
            raise LutrisGuildWars2NotFound(('Unable to find a game with name matching "Guild Wars 2", '
                                            'no Lutris ID set in config'))

        def start(self):
            """Load environment from the Lutris object, exec into the game."""
            if not self.lutris_installed:
                raise LutrisNotInstalled('Unable to import lutris libraries in system namespace.')
            if not self.installed:
                raise LutrisGuildWars2NotFound('Unable to identify Lutris Game ID from any source.')
            _ = self.lutris_game.runner.prelaunch()
            args, env = self.get_launch_parameters(
                self.lutris_game.runner, self.lutris_game.get_gameplay_info()
            )
            self.logger.info('Extending environment')
            self.logger.debug(env)
            os.environ.update(env)
            command = shutil.which(args[0])
            self.logger.info('Running command')
            self.logger.debug(command)
            sys.stdout.flush()
            sys.stderr.flush()
            # Disable bandit checks on launching a process without a shell
            #   Given such a carefully constructed environment and argument set,
            #   this seems wholly unnecessary to load another process into RAM
            os.execv(command, args)  # nosec

        @property
        def gamedir(self):
            """Return the directory that the game binary is in."""
            if not self.lutris_installed:
                raise LutrisNotInstalled('Unable to find lutris gamedir automatically without a Lutris installation.')
            if not self.installed:
                raise LutrisGuildWars2NotFound('Unable to find Lutris game matching Guild Wars 2.')
            return Path(self.lutris_game.config.game_config.get('exe')).parent

        @property
        def datdir(self):
            """Return the directory that the Local.dat file is in."""
            if not self.lutris_installed:
                raise LutrisNotInstalled('Unable to identify Local.dat directory without Lutris installed.')
            if not self.installed:
                raise LutrisGuildWars2NotFound('Unable to identify Local.dat direcotry withou knowing Lutris game id.')
            prefix = Path(self.lutris_game.config.game_config.get('prefix'))
            for candidate in prefix.rglob('Local.dat'):
                return candidate.parent
            for candidate in prefix.rglob('Guild Wars 2'):
                if 'AppData' in str(candidate):
                    return candidate
            raise FileNotFoundError('Unable to ascertain datdir for {prefix}. Consider hardcoding.')

    class SteamGuildWars2(object):
        """Sets the start function and gamedir property from the Steam configuration."""

        def __init__(self, config: Config):
            """Initialize a Steam game from the discovered VDF files."""
            user_specified_path = getattr(getattr(config.loaded.game, 'steam', None), 'dot_steam_folder', None)
            base_folder = Path(user_specified_path or '~/.steam').expanduser().resolve()
            self.base_folder = base_folder
            self.steam_registry = base_folder.joinpath('registry.vdf')
            self.game_id = 1284210
            try:
                import vdf
                self.vdf = vdf
            except ModuleNotFoundError:
                logger.error('gw2 was not installed with optional "steam" dependencies, unable to load game data.')

        @classmethod
        def _reg_find(cls, data: dict, search: str):
            """Search through a dictionary with a search string in dot notation."""
            for key in search.split('.'):
                data = data.get(key, {})
            return data

        @property
        def installed(self):
            """Return True when Guild Wars 2 is installed."""
            if self.steam_registry.exists():
                try:
                    with open(self.steam_registry) as f:
                        registry = self.vdf.load(f)
                except AttributeError:
                    logger.warning('Unable to properly read registry.vdf')
                    return False
                steam_gw2 = self._reg_find(registry, f'Registry.HKCU.Software.Valve.Steam.Apps.{self.game_id}')
                if steam_gw2 == {} or not bool(int(steam_gw2.get('Installed', '0'))):
                    logger.info('Unable to identify Guild Wars 2 installed in Steam registry.')
                    return False
                logger.info('Found Guild Wars 2 in Steam registry.')
                return True
            else:
                logger.error(f'Unable to locate the Steam registry.vdf file in {self.base_folder}')
                return False

        def start(self):
            """Start a game through steam."""
            logger.info('Starting Guild Wars 2 in Steam.')
            sys.stdout.flush()
            sys.stderr.flush()
            if self.installed:
                _ = os.system(f'(setsid steam steam://rungameid/{self.game_id} &) &>/dev/null')  # nosec
            else:
                raise SteamGuildWars2NotFound('Unable to identify Guild Wars 2 installation in Steam registry.')

        @property
        def gamedir(self):
            """Return the directory that the game binary is in."""
            library_folders_path = self.base_folder.joinpath('steam', 'steamapps', 'libraryfolders.vdf')
            if not library_folders_path.exists():
                raise FileNotFoundError(
                    f'Unable to locate the Steam libraryfolders.vdf in {library_folders_path.parent}'
                )
            with open(library_folders_path) as f:
                library_folders = self.vdf.load(f)
            for i, folder in library_folders.get('libraryfolders', {}).items():
                for appid, _ in folder.get('apps', {}).items():
                    if int(appid) == self.game_id:
                        game_path = Path(folder['path']).joinpath('steamapps', 'common', 'Guild Wars 2')
                        if game_path.exists() and game_path.joinpath('Gw2-64.exe').exists():
                            return game_path
            raise SteamGuildWars2NotFound('Unable to find Guild Wars 2 installation directory in Steam library.')

        @property
        def datdir(self):
            """Return the directory that Local.dat is in."""
            prefix = self.base_folder.joinpath('steam', 'steamapps', 'compatdata', str(self.game_id), 'pfx', 'drive_c')
            for candidate in prefix.rglob('Local.dat'):
                return candidate.parent
            for candidate in prefix.rglob('Guild Wars 2'):
                return candidate
            raise FileNotFoundError('Unable to ascertain datdir for {prefix}. Consider hardcoding.')
