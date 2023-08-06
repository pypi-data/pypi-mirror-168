from __future__ import annotations

import logging
import os
from pathlib import Path

import typer

from . import (
    collect_imports,
    collect_installed_packages,
    get_package_versions,
    write_requirements_in,
    write_requirements_txt,
)

app = typer.Typer()
logger = logging.getLogger(__name__)


@app.command()
def main(
    in_path: Path | None = None,
    out_path: Path | None = None,
    verbose: bool = False,
) -> None:
    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    if in_path is None:
        in_path = Path(".")
    if out_path is None:
        out_path = Path(os.getcwd())

    logger.info(f"Using {in_path} to search for project files")
    logger.info(f"Using {out_path} as target folder for requirement files")

    imports = collect_imports(in_path)
    env = collect_installed_packages()
    pkg_versions = get_package_versions(imports, env)
    write_requirements_in(out_path, pkg_versions)
    write_requirements_txt(out_path)


if __name__ == "__main__":
    app()
