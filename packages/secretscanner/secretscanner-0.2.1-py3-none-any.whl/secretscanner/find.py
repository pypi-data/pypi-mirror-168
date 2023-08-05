"""Find secrets within data"""

import re

from ppuri import uri

from secretscanner.types import SecretFormat


def find_re_secret(data: str, regex: str) -> list[str]:
    """Look for text matching a regular expression"""
    regex = f"({regex})"  # parse into a match group
    return [match.group(0) for match in re.finditer(regex, data, flags=re.IGNORECASE)]


def find_url_secret(data: str, scheme: str | None = None) -> list[str]:
    """Look for a URL with a password matching the scheme if specified"""
    matches = list(uri.scan(data))
    found: list[str] = []
    if matches:
        for match in matches:
            if scheme is None:
                found.append(match["uri"])
            else:
                if match["scheme"] == scheme:
                    if "password" in match["authority"]:
                        found.append(match["uri"])

    return found


def find_secrets(data: str, secret_format: SecretFormat) -> list[str]:
    """Find all secrets within the data"""
    if secret_format["type"] == "url":
        return find_url_secret(data, scheme=secret_format["format"])

    return find_re_secret(data, secret_format["format"])
