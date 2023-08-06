"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the CLI functions for profile management.
"""

from .main import main
from .util import GW2CLIUtils, click, theme


@main.group(cls=GW2CLIUtils.AliasedGroup, invoke_without_command=True)
@GW2CLIUtils.verbose_opt
@GW2CLIUtils.config_opt
@click.pass_context
def profile(ctx, verbose, config_path):
    """Run the profile management interface for Gee Whiz 2."""
    logger = GW2CLIUtils.make_logger(verbose)
    logger.debug('Profile management group')
    try:
        if config_path is not None:
            ctx.obj = GW2CLIUtils.Config(config_path=config_path)
        profiles = GW2CLIUtils.GuildWars2Profiles(config=ctx.obj)
        if ctx.invoked_subcommand is None:
            GW2CLIUtils.print(f'Current profile: [{theme.blue}]{profiles.current}[/{theme.blue}]')
            yaml = ''
            for profile in profiles:
                yaml += f'- {profile}\n'
            GW2CLIUtils.yaml_print(yaml.strip(), name='Available profiles:')
            original_command = []
            working = ctx
            while working is not None:
                original_command.insert(0, working.info_name)
                working = working.parent
            GW2CLIUtils.print(
                f'\nFor more information, run: [{theme.red}]{" ".join(original_command)} -h[/{theme.red}].')
    except Exception as e:
        GW2CLIUtils.handle(e, ctx)


@profile.command()
@GW2CLIUtils.verbose_opt
@GW2CLIUtils.config_opt
@click.argument('profile_name', nargs=-1)
@click.option('-s', '--set-current', is_flag=True, default=False,
              help=('Set the newly created profile as the current one immediately. '
                    '(may behave poorly if multiple are specified)'))
@click.pass_context
def add(ctx, verbose, config_path, profile_name, set_current):
    """Create and manage PROFILE_NAME."""
    logger = GW2CLIUtils.make_logger(verbose)
    logger.debug('Profile add command')
    try:
        if config_path is not None:
            ctx.obj = GW2CLIUtils.Config(config_path=config_path)
        profiles = GW2CLIUtils.GuildWars2Profiles(config=ctx.obj)
        for profile in profile_name:
            profiles.add(profile)
            if set_current:
                profiles.set(profile)
    except Exception as e:
        GW2CLIUtils.handle(e, ctx)


@profile.command()
@GW2CLIUtils.verbose_opt
@GW2CLIUtils.config_opt
@click.argument('profile_name', nargs=-1)
@click.pass_context
def remove(ctx, verbose, config_path, profile_name):
    """Remove PROFILE_NAME from management."""
    logger = GW2CLIUtils.make_logger(verbose)
    logger.debug('Profile rm command')
    try:
        if config_path is not None:
            ctx.obj = GW2CLIUtils.Config(config_path=config_path)
        profiles = GW2CLIUtils.GuildWars2Profiles(config=ctx.obj)
        for profile in profile_name:
            profiles.rm(profile)
    except Exception as e:
        GW2CLIUtils.handle(e, ctx)


@profile.command()
@GW2CLIUtils.verbose_opt
@GW2CLIUtils.config_opt
@click.argument('profile_name', nargs=1)
@click.pass_context
def set(ctx, verbose, config_path, profile_name):
    """Set PROFILE_NAME as the currently active profile."""
    logger = GW2CLIUtils.make_logger(verbose)
    logger.debug('Profile set command')
    try:
        if config_path is not None:
            ctx.obj = GW2CLIUtils.Config(config_path=config_path)
        profiles = GW2CLIUtils.GuildWars2Profiles(config=ctx.obj)
        profiles.set(profile_name)
    except Exception as e:
        GW2CLIUtils.handle(e, ctx)


@profile.command()
@GW2CLIUtils.verbose_opt
@GW2CLIUtils.config_opt
@click.pass_context
def list(ctx, verbose, config_path):
    """List all profiles under management."""
    logger = GW2CLIUtils.make_logger(verbose)
    logger.debug('Profile ls command')
    try:
        if config_path is not None:
            ctx.obj = GW2CLIUtils.Config(config_path=config_path)
        profiles = GW2CLIUtils.GuildWars2Profiles(config=ctx.obj)
        for profile in profiles:
            GW2CLIUtils.print(profile)
    except Exception as e:
        GW2CLIUtils.handle(e, ctx)
