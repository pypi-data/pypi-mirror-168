import json
import logging
import os
import sys
import traceback
from pathlib import Path

import click
from pydantic import ValidationError

from chalk import importer
from chalk.config.project_config import ProjectSettings, load_project_config
from chalk.parsed.user_types_to_json import get_registered_types_as_json


@click.group()
@click.option(
    "--log-level",
    default="info",
    help="The logging level. One of DEBUG, INFO, WARNING, ERROR, and CRITICAL (case-insensitive).",
)
def cli(log_level: str):
    level = getattr(logging, log_level.upper())
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=level,
    )


@cli.command("list")
@click.argument(
    "directory",
    default=None,
    required=False,
)
def list_cmd(directory):
    scope_to = Path(directory or os.getcwd())
    try:
        failed = importer.import_all_python_files()
        print(get_registered_types_as_json(scope_to, failed))
    except Exception:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        relevant_traceback = f"""{os.linesep.join(traceback.format_tb(ex_traceback))}
\n{ex_type.__name__}: {str(ex_value)}
"""
        print(json.dumps(dict(failed=[dict(traceback=relevant_traceback)]), indent=2))


@cli.command("config")
def config():
    json_response: str
    try:
        model = load_project_config() or ProjectSettings()
        json_response = model.json()
    except ValidationError as e:
        json_response = json.dumps({"error": str(e)})

    print(json_response)


if __name__ == "__main__":
    cli()
