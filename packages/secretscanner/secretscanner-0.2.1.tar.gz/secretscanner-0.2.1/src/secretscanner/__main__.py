#!/usr/bin/python3
"""Secret Scanner command line interface"""
import sys
from pathlib import Path

import click
import rich

from secretscanner.report import json_report, report
from secretscanner.scanner import scan


@click.command()
@click.argument("directory", type=click.Path())
@click.option(
    "-v",
    "--verbose",
    default=False,
    is_flag=True,
    help="If set includes information on the secrets in the report.",
)
@click.option(
    "-q", "--quiet", default=False, is_flag=True, help="If set no output is printed."
)
@click.option(
    "-j",
    "--json",
    default=False,
    is_flag=True,
    help="If set the report is output as json.",
)
def run(
    directory: click.Path,
    verbose: bool,
    quiet: bool,
    json: bool,
):
    """Scan a directory for secrets."""
    scan_dir = Path(str(directory)).expanduser().resolve()
    if not scan_dir.exists():
        rich.print(f"Directory {directory} not found.")

    results = scan(scan_dir, quiet)
    if not quiet and results is not None:
        if not json:
            report(results, verbose)
        else:
            json_report(results)

    if results and len(results["secrets"]) != 0:
        sys.exit(1)
    else:
        sys.exit(0)


run()
