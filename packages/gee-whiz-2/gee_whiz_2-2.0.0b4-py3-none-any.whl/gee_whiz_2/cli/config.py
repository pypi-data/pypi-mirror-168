"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the CLI functions for config management.
"""

from .main import main
from .util import GW2CLIUtils, click, theme


@main.group(cls=GW2CLIUtils.AliasedGroup, invoke_without_command=True)
@GW2CLIUtils.verbose_opt
@GW2CLIUtils.config_opt
@click.pass_context
def config(ctx, verbose, config_path):
    """Run the configuration management interface for Gee Whiz 2."""
    logger = GW2CLIUtils.make_logger(verbose)
    logger.debug('Config management group')
    try:
        if config_path is not None:
            ctx.obj = GW2CLIUtils.Config(config_path=config_path)
        if ctx.invoked_subcommand is None:
            GW2CLIUtils.print(f'Loaded from: {"<default>" if ctx.obj.loaded_from is None else ctx.obj.loaded_from}')
            GW2CLIUtils.yaml_print(ctx.obj.loaded.yaml().strip(), name='Current config:')
            GW2CLIUtils.print(
                f'\nFor more information, run: [{theme.red}]{ctx._original_command()} -h[/{theme.red}].')
    except Exception as e:
        GW2CLIUtils.handle(e, ctx)


@config.command()
@GW2CLIUtils.verbose_opt
@GW2CLIUtils.config_opt
@click.pass_context
def show(ctx, verbose, config_path):
    """Output the configuration only."""
    logger = GW2CLIUtils.make_logger(verbose)
    logger.debug('Config show command')
    try:
        if config_path is not None:
            ctx.obj = GW2CLIUtils.Config(config_path=config_path)
        GW2CLIUtils.print(ctx.obj.loaded.yaml().strip())
    except Exception as e:
        GW2CLIUtils.handle(e, ctx)


@config.command(short_help='Change a configuration option.',
                epilog=('WARNING: When updating your saved config, '
                        'all values with a default will be populated with the defaults.'))
@GW2CLIUtils.verbose_opt
@GW2CLIUtils.config_opt
@click.argument('config_key', nargs=1)
@click.argument('config_value', nargs=1)
@click.pass_context
def set(ctx, verbose, config_path, config_key, config_value):
    """Set CONFIG_KEY to CONFIG_VALUE in the loaded configuration, traversing paths with . and [#] notation."""
    logger = GW2CLIUtils.make_logger(verbose)
    logger.debug('Config set command')
    try:
        if config_path is not None:
            ctx.obj = GW2CLIUtils.Config(config_path=config_path)
        config_path = ctx.obj.loaded_from
        if config_path is None:
            raise click.ClickException('Unable to change the configuration as it was not loaded from anywhere.')
        config_item = ctx.obj.loaded
        logger.info(f'Existing config: {config_item}')
        nested_keys = config_key.split('.')
        if len(nested_keys) > 1:
            for ref in nested_keys[:-1]:
                config_item = getattr(config_item, ref)
        logger.debug(type(config_item))
        setattr(config_item, nested_keys[-1], config_value)
        logger.info(f'New config: {ctx.obj.loaded}')
        GW2CLIUtils.print(f'Writing config back to {config_path}...')
        with open(config_path, 'w') as f:
            f.write(ctx.obj.loaded.yaml())
        ctx.obj.load_config(config_path=config_path)
    except Exception as e:
        GW2CLIUtils.handle(e, ctx)


@config.command()
@GW2CLIUtils.verbose_opt
@GW2CLIUtils.config_opt
@click.pass_context
def path(ctx, verbose, config_path):
    """Output the autoloaded config path."""
    logger = GW2CLIUtils.make_logger(verbose)
    logger.debug('Config path command')
    try:
        if config_path is not None:
            ctx.obj = GW2CLIUtils.Config(config_path=config_path)
        config_path = ctx.obj.loaded_from
        GW2CLIUtils.print(f'Config was loaded from {config_path}')
    except Exception as e:
        GW2CLIUtils.handle(e, ctx)
