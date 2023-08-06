"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the CLI utility functions used in other modules.
"""

import rich_click as click
from click import Context
from pathlib import Path
from rich.panel import Panel
from rich.syntax import Syntax

from ..addon import GeeWhiz2AddonArcDPS, GeeWhiz2AddonArcDPSExtra, extras
from ..config import Config
from ..game import GuildWars2
from ..profiles import GuildWars2Profiles
from ..util import console, make_logger, theme


# Add a function to the context to make it easier for subcommands
#   to reconstruct the command they were called with.
def _original_command(self):
    working = self
    original_command = []
    while working is not None:
        original_command.insert(0, working.info_name)
        working = working.parent
    original_command = " ".join(original_command)
    return original_command


Context._original_command = _original_command


click.rich_click.STYLE_OPTION = theme.fg
click.rich_click.STYLE_ARGUMENT = theme.green
click.rich_click.STYLE_SWITCH = theme.subtle
click.rich_click.STYLE_METAVAR = theme.green
click.rich_click.STYLE_USAGE = theme.blue


class GW2CLIUtils(object):
    """This helper class wraps the methods used in the CLI."""

    Config = Config
    GuildWars2 = GuildWars2
    make_logger = make_logger
    GuildWars2Profiles = GuildWars2Profiles
    print = console.print
    rule = console.rule

    class AliasedGroup(click.RichGroup):
        """A custom Rich Click group which will resolve short names."""

        def get_command(self, ctx, cmd_name):
            """Return a command in the group if it uniquely matches the first characters provided."""
            rv = click.Group.get_command(self, ctx, cmd_name)
            if rv is not None:
                return rv
            matches = [x for x in self.list_commands(ctx)
                       if x.startswith(cmd_name)]
            if not matches:
                return None
            elif len(matches) == 1:
                return click.Group.get_command(self, ctx, matches[0])
            ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

        def resolve_command(self, ctx, args):
            """Return the full command name."""
            _, cmd, args = super().resolve_command(ctx, args)
            return cmd.name, cmd, args

    @staticmethod
    def yaml_print(yaml: str, number: bool = False, name: str = None):
        """Print YAML with syntax highlighting."""
        syntax = Syntax(yaml, 'yaml', line_numbers=number, tab_size=2, indent_guides=True, theme=theme.pygment)
        console.print(
            Panel.fit(
                syntax,
                title=name,
                title_align='left',
                border_style=f'{theme.fg} on {theme.bg}'
            ),
            style=f'white on {theme.bg}'
        )

    @staticmethod
    def verbose_opt(func):
        """Wrap the func with a common verbosity argument."""
        return click.option(
            '-v', '--verbose', count=True,
            help='Increase verbosity (specify multiple times for more)'
        )(func)

    @staticmethod
    def config_opt(func):
        """Wrap the func with a common config argument."""
        return click.option(
            '-c', '--config', 'config_path', type=Path,
            help='A specific config to load'
        )(func)

    @staticmethod
    def update_all_addons(config: Config):
        """Update all addons, using the appropriate interface for the current config."""
        logger = make_logger()
        if config is None:
            config = Config()
        arcdps = GeeWhiz2AddonArcDPS(config=config)
        arcdps.update()
        for extra in extras:
            addon = GeeWhiz2AddonArcDPSExtra(config=config, **extra)
            addon.update()
        logger.info('All addon updates completed successfully.')

    @staticmethod
    def choose_profile(config: Config):
        """Choose a profile from the selection of available profiles."""
        logger = make_logger()
        if config is None:
            config = Config()
        profiles = GuildWars2Profiles(config=config)
        old_profile = profiles.current
        picker = config.picker(options=[str(p) for p in profiles], current=str(old_profile))
        new_profile = picker.choose()
        indicator = config.status(text=f'Saving {old_profile} and installing {new_profile}').indicator
        with indicator:
            profiles.set(new_profile)
        logger.info(f'Profile set to {new_profile}')

    @staticmethod
    def handle(e: Exception, ctx: click.Context):
        """Handle exceptions depending on the verbosity level."""
        logger = make_logger()
        original_command = []
        working = ctx
        while working is not None:
            original_command.insert(0, working.info_name)
            working = working.parent
        original_command = " ".join(original_command)
        if logger.handlers[0].level < 20:
            logger.exception(f'Problem executing "{original_command}" with {ctx.params}')
            exit(1)
        else:
            raise click.ClickException(str(e))
