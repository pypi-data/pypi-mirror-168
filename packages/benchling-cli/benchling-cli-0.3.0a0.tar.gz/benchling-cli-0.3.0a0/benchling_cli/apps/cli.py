import os
from pathlib import Path
import shutil

from benchling_sdk.apps.helpers.manifest_helpers import manifest_from_file
import typer

from benchling_cli.apps.codegen.generate_dependencies_module import generate_dependencies_module
from benchling_cli.apps.codegen.generate_models import generate_models

apps_cli = typer.Typer()


DEFAULT_MANIFEST_FILE_PATH = "manifest.yaml"
DEFAULT_DEPENDENCIES_FILE_PATH = "dependencies.py"
DEFAULT_MODEL_DIRECTORY_PATH = "generated_models"
MANIFEST_OPTION = typer.Option(DEFAULT_MANIFEST_FILE_PATH, "--manifest-file-path", "-m")


@apps_cli.command(
    name="dependencies",
    help="App dependencies generation allows a Benchling App to depend on resources within a tenant in a portable way, "
    "without hard-coding the API IDs.",
)
def dependencies(
    manifest_file_path: str = MANIFEST_OPTION,
    dependencies_file_path: str = DEFAULT_DEPENDENCIES_FILE_PATH,
    model_directory_path: str = DEFAULT_MODEL_DIRECTORY_PATH,
):
    """Auto-generate Python code for accessing your App's dependencies at run-time."""
    manifest = manifest_from_file(Path(manifest_file_path))
    if not manifest.configuration:
        typer.echo("Skipping code generation because the manifest has no dependencies.")
        return

    if os.path.exists(dependencies_file_path):
        typer.echo(f"Overwriting existing dependency file {dependencies_file_path}")
    else:
        typer.echo(f"Creating new dependency file {dependencies_file_path}")

    with open(dependencies_file_path, "w") as f:
        f.write(generate_dependencies_module(manifest))

    # Version is not currently part of the manifest model
    optional_version = manifest.info.get("version", "")

    typer.secho(
        f"Success! Generated dependency file for {manifest.info.name} {optional_version} "
        f"at {dependencies_file_path}.",
        fg="green",
    )

    if os.path.exists(model_directory_path):
        shutil.rmtree(model_directory_path)
        typer.echo(f"Removing existing directory {model_directory_path}")

    typer.echo(f"Creating model files in new directory {model_directory_path}")
    os.mkdir(model_directory_path)
    with open(os.path.join(model_directory_path, "__init__.py"), "w") as f:
        f.write("")

    for model_name, model_file in generate_models(manifest).items():
        file_path = os.path.join(model_directory_path, f"{model_name}.py")
        with open(file_path, "w") as f:
            f.write(model_file)
            typer.secho(
                f"Success! Generated model file at {file_path}",
                fg="green",
            )
