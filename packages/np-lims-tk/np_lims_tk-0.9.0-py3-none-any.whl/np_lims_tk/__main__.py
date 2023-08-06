from typing import Optional

import json
from random import choice

import typer
from rich.console import Console

from np_lims_tk import core, exceptions, version

app = typer.Typer(
    name="np_lims_tk",
    help="Awesome `np_lims_tk` is a Python cli/package created with https://github.com/TezRomacH/python-package-template",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]np-lims-tk[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command(name="")
def main(
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the np_lims_tk package.",
    ),
) -> None:
    """Print version."""


@app.command()
def find_lims_files(
    filepaths_json: str,
    output_path: str,
    db_uri: Optional[str] = typer.Option(
        None,
        "-d",
        "--db-uri",
        help="Database uri for lims connection. If not supplied, defaults to allen_config_auto_discovery.",
    ),
) -> None:
    with open(filepaths_json) as f:
        filepaths = json.load(f)

    results = []
    for filepath in filepaths:
        try:
            found = core.find_files(
                db_uri=db_uri,
                local_path=filepath,
            )
            error = None
        except Exception as e:
            found = None
            error = str(e)

        result = {
            "filepath": filepath,
            "found": found,
            "error": error,
        }
        results.append(result)

    with open(output_path, "w") as f:
        json.dump(
            results,
            f,
            sort_keys=True,
            indent=4,
        )


@app.command()
def path_to_data_manifestor_meta(
    path: str,
    output_path: str,
    db_uri: Optional[str] = typer.Option(
        None,
        "-d",
        "--db-uri",
        help="Database uri for lims connection. If not supplied, defaults to allen_config_auto_discovery.",
    ),
    manifestor_lookup_path: Optional[str] = typer.Option(
        None,
    ),
) -> None:
    if manifestor_lookup_path:
        with open(manifestor_lookup_path) as f:
            manifestor_lookup = json.load(f)
    else:
        manifestor_lookup = None

    lims_meta = core.path_to_lims_meta(path)
    if not lims_meta:
        raise exceptions.NPTKError("No lims meta inferred from path: %s" % path)

    lims_id = lims_meta._id
    project_name = core.get_project_name(
        lims_id=lims_id,
        db_uri=db_uri,
    )

    if not project_name:
        raise exceptions.NPTKError(
            "Couldnt find associated project name. lims_id={}, db_uri={}".format(
                lims_id, db_uri
            )
        )

    template_path = core.project_name_to_data_manifestor_template(
        project_name,
        manifestor_lookup=manifestor_lookup,
        raw=True,
    )

    meta = {
        "lims_id": lims_id,
        "subject_id": lims_meta.subject_id,
        "date_str": lims_meta.date_str,
        "project_name": project_name,
        "manifestor_template_path": template_path,
    }

    with open(output_path, "w") as f:
        json.dump(meta, f)


if __name__ == "__main__":
    app()
