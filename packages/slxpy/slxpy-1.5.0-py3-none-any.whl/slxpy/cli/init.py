from pathlib import Path

import click


@click.command()
@click.pass_context
def init(ctx: click.Context):
    """
    Initialize slxpy working directory.
    """
    workdir: Path = ctx.obj["workdir"]

    from slxpy.frontend.init import init_interactive
    init_interactive(workdir)
