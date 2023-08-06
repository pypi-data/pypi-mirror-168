"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the main CLI entrypoint.
"""

from .util import GW2CLIUtils, click, theme


@click.group(
    cls=GW2CLIUtils.AliasedGroup,
    context_settings=dict(help_option_names=["-h", "--help"]),
    invoke_without_command=True
)
@GW2CLIUtils.verbose_opt
@GW2CLIUtils.config_opt
@click.option('-s/-n', '--start/--no-start', default=None, help='Start Guild Wars 2 after processing.')
@click.option('-p/-P', '--profile/--no-profile', default=None,
              help='Prompt for profile selection if profiles are available.')
@click.option('-f', '--force', is_flag=True,
              help='Force start even if update fails (if the game is configured/selected to start).')
@click.version_option(None, '--version', '-V')
@click.pass_context
def main(ctx, config_path, start, force, profile, verbose):
    """Run the primary CLI for Gee Whiz 2.

    If no additional commands are specified, updates will be run according to your configuration.
    """
    logger = GW2CLIUtils.make_logger(verbose)
    logger.debug(f'start: {start}')

    try:
        ctx.obj = GW2CLIUtils.Config(config_path=config_path)
        if ctx.invoked_subcommand is None:
            GW2CLIUtils.rule('Checking for updates')
            try:
                GW2CLIUtils.update_all_addons(config=ctx.obj)
            except Exception as e:
                if force:
                    GW2CLIUtils.print(f'Update failed: {e}')
                else:
                    raise e

            if start or (ctx.obj.loaded.start_gw2 and start is not False):
                if profile or (ctx.obj.loaded.profile_prompt and profile is not False):
                    if len(ctx.obj.state.profiles.available) > 1:
                        GW2CLIUtils.rule('Setting current profile')
                        GW2CLIUtils.choose_profile(config=ctx.obj)
                GW2CLIUtils.print((
                    f'Starting [{theme.red}]Guild Wars 2[/{theme.red}] '
                    f'via {ctx.obj.loaded.game.type}...'
                ))
                gw2 = GW2CLIUtils.GuildWars2(config=ctx.obj)
                gw2.start()
    except Exception as e:
        GW2CLIUtils.handle(e, ctx)
