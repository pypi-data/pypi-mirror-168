"""Type definitions"""
from typing import TypedDict

SecretIssuer = str
IssuerSecretFormats = dict[SecretIssuer, str]


class SecretFormat(TypedDict):
    """Information on how to match a secret"""

    type: str
    format: str


# SecretFormat = str
SecretType = str
SecretParseInfo = dict[SecretType, SecretFormat]
SecretIssuerParseInfo = dict[SecretIssuer, SecretParseInfo]


class Secret(TypedDict):
    """Information about a secret"""

    file: str
    issuer: SecretIssuer
    secret: str
    type: SecretType
    ignored: bool


SecretResults = list[Secret]


class ScanResults(TypedDict):
    """Results of the secret scan"""

    file_count: int
    scan_time: int
    secrets: SecretResults
