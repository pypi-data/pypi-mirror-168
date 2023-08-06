from typing import Optional

import json
from enum import Enum
from random import choice

import typer
import yaml
from rich.console import Console

from data_manifestor import core, exceptions, version


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


app = typer.Typer(
    name="data_manifestor",
    help="Awesome `data_manifestor` is a Python cli/package created with https://github.com/TezRomacH/python-package-template",
    add_completion=False,
)
console = Console()


def dump_object_to_file(value, path):
    with open(path, "w") as f:
        json.dump(
            value,
            f,
            sort_keys=True,
            indent=4,
        )


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]data_manifestor[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command(name="")
def main(
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the data_manifestor package.",
    ),
) -> None:
    """Prints version."""


@app.command()
def find_files(
    directory: str,
    template_path: str,
    lims_id: str,
    subject_id: str,
    date_str: str,
    output_path: str,
    missing_output_path: str,
    fail_if_missing: bool = typer.Option(
        None,
        "-f",
        "--fail",
        help="Raise an exception if files are missing.",
    ),
) -> None:
    with open(template_path) as f:
        template = yaml.safe_load(f)

    results = core.compare_manifest_to_local(
        directory,
        lims_id,
        subject_id,
        date_str,
        template_dict=template,
    )

    found = []
    missing = []
    for (
        pattern,
        paths,
    ) in results.resolved_paths:
        if not len(paths) > 0:
            missing.append(pattern)
        else:
            found.extend(paths)

    dump_object_to_file(
        found,
        output_path,
    )

    dump_object_to_file(
        missing,
        missing_output_path,
    )

    if fail_if_missing and len(missing) > 0:
        raise exceptions.PathError("Path not found for: %s" % pattern)


if __name__ == "__main__":
    app()
