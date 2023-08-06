from importlib.metadata import version
from typing import Optional

import typer

from benchling_cli.apps.cli import apps_cli


def _version_callback(value: bool) -> None:
    if value:
        package_version = version("benchling-cli")
        typer.echo(f"Benchling CLI version: {package_version}")
        raise typer.Exit()


cli = typer.Typer()


@cli.callback()
def callback(
    version_option: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Displays the version of Benchling CLI and exits",
    )
):
    pass


cli.add_typer(
    apps_cli,
    name="app",
    help="Benchling apps are portable and transferable integrations administered within Benchling.",
)
