from typing import Literal, Optional

import json
import logging
from enum import Enum
from random import choice
from uuid import uuid4

import typer
import yaml
from rich.console import Console

from np_validator import version
from np_validator.core import autogenerate_validation_steps, run_validation
from np_validator.dataclasses import dump_ValidationResult, load_ValidationStep

run_id = uuid4().hex
log_filepath = f"np-validator-{run_id}.log"

logging.basicConfig(
    filename=log_filepath,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

app = typer.Typer(
    name="np_validator",
    help="Awesome `np_validator` is a Python cli/package created with https://github.com/TezRomacH/python-package-template",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]np_validator[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command(name="")
def main(
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the np_validator package.",
    ),
) -> None:
    """Prints version"""


@app.command()
def validate(
    file_list_path: str,
    results_path: str,
    validation_steps_path: str = typer.Option(
        None,
    ),
) -> None:
    with open(file_list_path) as f:
        file_list = json.load(f)

    if validation_steps_path:
        with open(validation_steps_path) as f:
            validation_steps = [
                load_ValidationStep(step_dict)
                for step_dict in yaml.load(  # nosec: getting depreciated anyway
                    f.read(), Loader=yaml.Loader
                )
            ]
    else:
        validation_steps = autogenerate_validation_steps(file_list)

    try:
        results = run_validation(
            file_list,
            validation_steps,
            autogen_steps=False,
        )
    except Exception as e:
        console.print(f"Failed validation. Saving log to:\n\t{log_filepath}")
        logger.error(e, exc_info=True)
        return

    with open(results_path, "w") as f:
        json.dump(
            [dump_ValidationResult(result) for result in results],
            f,
            sort_keys=True,
            indent=4,
        )


if __name__ == "__main__":
    app()
