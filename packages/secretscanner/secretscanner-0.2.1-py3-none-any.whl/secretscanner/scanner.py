"""Secret scanning"""
from pathlib import Path
from typing import Generator
import concurrent.futures

from rich.progress import Progress

from secretscanner.secret_info import secret_issuer_parse_info
from secretscanner.find import find_secrets
from secretscanner.gitignore import set_ignored_flag
from secretscanner.types import (
    Secret,
    SecretResults,
    ScanResults,
)
from secretscanner.progress_column_file import FileColumn


def file_filter(path: Path):
    """Filter out files before processing"""
    if not "__pycache__" in str(path):
        return path


def walk(path: Path) -> Generator[str, None, None]:
    """Walk a path and return all files found"""
    for entry in Path(path).iterdir():
        if entry.is_dir():
            yield from walk(entry)
            continue

        if entry.stat().st_size <= 0:
            continue

        resolved = entry.resolve()
        if file_filter(resolved):
            yield str(resolved)


def scan(scan_path: Path, quiet: bool = False) -> ScanResults | None:
    """Scan a path for secrets"""
    if scan_path.is_file():
        files = [str(scan_path)]
    else:
        files = list(walk(scan_path))

    if not files:
        return None

    file_count = len(files)
    finished_time = 0
    found: SecretResults = []

    if file_count == 1:
        found = scan_file(files[0])
    else:
        if quiet:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                future_to_scan = {
                    executor.submit(scan_file, filename): filename for filename in files
                }
                for future in concurrent.futures.as_completed(future_to_scan):
                    secrets = future.result()
                    found += secrets
        else:
            completed = 0
            file_progress_column = FileColumn(files, root_path=str(scan_path))
            with Progress(
                *Progress.get_default_columns(), file_progress_column
            ) as progress:
                progress_task = progress.add_task("Scanning...", total=file_count)
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    future_to_scan = {
                        executor.submit(scan_file, filename): filename
                        for filename in files
                    }
                    for future in concurrent.futures.as_completed(future_to_scan):
                        secrets = future.result()
                        found += secrets
                        completed += 1
                        progress.update(progress_task, completed=completed)

                progress_task = progress._tasks[progress_task]  # type: ignore

            finished_time = int(progress_task.finished_time or 0)

    if found:
        set_ignored_flag(found, scan_path)

    results: ScanResults = {
        "file_count": file_count,
        "scan_time": finished_time,
        "secrets": found,
    }
    return results


def scan_file(file_to_scan: str) -> SecretResults:
    """Scan a single file for secrets"""
    found: SecretResults = []

    with open(file_to_scan, mode="r") as fileptr:  # type: ignore
        try:
            data = fileptr.read(-1)  # type: ignore
        except UnicodeDecodeError:
            return []

    for issuer, secret_info in secret_issuer_parse_info.items():
        for secret_type, secret_format in secret_info.items():
            secrets = find_secrets(data, secret_format)  # type: ignore

            if secrets:
                for secret_text in secrets:
                    secret: Secret = {
                        "file": str(file_to_scan),
                        "issuer": issuer,
                        "type": secret_type,
                        "secret": secret_text,
                        "ignored": False,
                    }
                    found.append(secret)

    return found
