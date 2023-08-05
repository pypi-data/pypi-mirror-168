"""Use .gitignore to determine files that rely on an entry to stop
them being pushed to a repository
"""
from pathlib import Path
from typing import Iterable

import pathspec

from secretscanner.types import SecretResults


def rfindfile(filename: str, path: Path | None = None) -> Path | None:
    """Scan for a filename moving up the directory tree"""
    if path is None:
        path = Path.cwd()

    while True:
        files = [p.name for p in path.glob("*")]
        if filename in files:
            return path / filename

        if path.parent == path:
            return None

        return rfindfile(filename, path.parent)


def gitignore_pathspec(gitignore: Path) -> pathspec.PathSpec:
    """Get a pathspec for the `.gitignore` file"""
    with open(gitignore, "r", encoding="utf-8") as gifp:
        gidata = gifp.readlines()
        spec = pathspec.PathSpec.from_lines(  # type: ignore
            pathspec.patterns.GitWildMatchPattern, gidata
        )
        return spec  # type: ignore


def gitignored(
    files: Iterable[str], directory: Path
) -> tuple[Iterable[str], Iterable[str]]:
    """Determine whether files are ignored by `.gitignore` or not"""
    gitignore_file = rfindfile(".gitignore", directory)
    if gitignore_file is not None:
        gitignore_spec = gitignore_pathspec(gitignore_file)
        ignored: list[str] = []
        notignored: list[str] = []
        for file in files:
            if gitignore_spec.match_file(file):  # type: ignore
                ignored.append(file)
            else:
                notignored.append(file)
        return ignored, notignored

    return files, []


def set_ignored_flag(secrets: SecretResults, directory: Path):
    """Set the ignored flag on a secret"""
    files = {t["file"] for t in secrets}
    if not files:
        return

    ignored, notignored = gitignored(files, directory)
    for secret in secrets:
        if secret["file"] in ignored and secret["file"] not in notignored:
            secret["ignored"] = True
        else:
            secret["ignored"] = False
