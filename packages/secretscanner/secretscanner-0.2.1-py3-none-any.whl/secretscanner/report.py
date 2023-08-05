"""Print scan report"""
import json
from collections import defaultdict
from textwrap import wrap
from typing import Any
from datetime import timedelta

import rich
import rich.console
from rich.text import Text

from secretscanner.highlighter import SecretHighlighter
from secretscanner.types import SecretResults, Secret, ScanResults

INDENT = "  "


def secretlist_to_file_dict(secrets: SecretResults) -> dict[str, list[Any]]:
    """Convert the list of secrets to a dict with file name as key."""
    files: dict[str, list[Any]] = defaultdict(list)
    for item in secrets:
        files[item["file"]].append(item)

    return files


def print_secret(secret: Secret, console: rich.console.Console):
    """Print the information on a single secret"""
    highlighter = SecretHighlighter()
    rich.print(f"{INDENT*2}- [blue]Issuer[/]: {secret['issuer']}")
    rich.print(f"{INDENT*2}  [blue]Type[/]: {secret['type']}")
    if len(secret["secret"]) + 20 < console.width:
        secret_text = secret["secret"].strip("\n")
        rich.print(f"{INDENT*2}  [blue]Secret[/]: ", end="")
        rich.print(highlighter(f"{secret_text}"))
    else:
        rich.print(f"{INDENT*2}  [blue]Secret[/]:")
        txt = wrap(
            secret["secret"],
            width=console.width - 4,
            initial_indent=INDENT * 3 + "  ",
            subsequent_indent=INDENT * 3 + "  ",
        )
        rich.print(highlighter("\n".join(txt)))


def print_scan_info(results: ScanResults):
    """Display number of files scanned plus scan time if > 0"""
    file_count = results["file_count"]
    if file_count == 1:
        print("1 file scanned")
        return

    print(f"{file_count} files scanned", end="")

    finished_time = results["scan_time"]
    if finished_time > 0:
        total_time = timedelta(seconds=finished_time)
        finished_time_text = Text(str(total_time), style="progress.elapsed")
        print(f" in {finished_time_text}")
    else:
        print()


def report(results: ScanResults, verbose: bool) -> None:
    """Print out report."""
    console = rich.console.Console()

    print_scan_info(results)

    secrets = results["secrets"]
    if not secrets:
        rich.print("[green]No secrets found[/]")
        return

    secret_to_file = secretlist_to_file_dict(secrets)

    if not verbose:
        rich.print("[yellow]Files with embedded secrets:[/]")
    else:
        rich.print("[yellow]Embedded secrets:[/]")

    for file, secrets_in_file in sorted(secret_to_file.items()):
        ignored = secrets_in_file[0]["ignored"]
        if ignored:
            color = "yellow"
            suffix = " [dim](ignored via .gitignore)[/]"
        else:
            if verbose:
                color = "blue"
            else:
                color = "yellow"
            suffix = ""

        rich.print(f"{INDENT}[{color}]{file}{suffix}[/]")
        if verbose:
            for secret in secrets_in_file:
                print_secret(secret, console)


def json_report(results: ScanResults) -> None:
    """Print out the secrets as a JSON formatted string."""
    if results["secrets"]:
        print(json.dumps(results["secrets"]))
