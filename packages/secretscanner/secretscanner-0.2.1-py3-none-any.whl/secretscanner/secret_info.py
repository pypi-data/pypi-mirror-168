"""Secret parsing information"""
from secretscanner.types import (
    SecretIssuerParseInfo,
    IssuerSecretFormats,
)

secret_format: IssuerSecretFormats = {
    "github": r"[A-Za-z0-9_]{36,251}",
    "digitalocean": r"[A-Za-z0-9_]{64,}",
    "adafruit": r"[A-Za-z0-9]{32}",
    "discord": r"[A-Za-z0-9]{32}",
    "linode": r"[A-Za-z0-9]{64}",
}

secret_issuer_parse_info: SecretIssuerParseInfo = {
    # https://github.blog/changelog/2021-03-31-authentication-secret-format-updates-are-generally-available/
    "github": {
        "pat": {
            "type": "re",
            "format": f"ghp_{secret_format['github']}",
        },
        "oauth": {
            "type": "re",
            "format": f"gho_{secret_format['github']}",
        },
        "user-to-server": {
            "type": "re",
            "format": f"ghu_{secret_format['github']}",
        },
        "server-to-server": {
            "type": "re",
            "format": f"ghs_{secret_format['github']}",
        },
        "refresh": {
            "type": "re",
            "format": f"ghr_{secret_format['github']}",
        },
    },
    "pypi": {
        "pat": {"type": "re", "format": "pypi-[A-Za-z0-9_]{16,}"},
    },
    # https://docs.digitalocean.com/reference/api/create-personal-access-secret/
    "digitalocean": {
        "pat": {
            "type": "re",
            "format": f"dop_v1_{secret_format['digitalocean']}",
        },
        "oauth": {
            "type": "re",
            "format": f"doo_v1_{secret_format['digitalocean']}",
        },
        "refresh": {
            "type": "re",
            "format": f"dor_v1_{secret_format['digitalocean']}",
        },
    },
    "postgresql": {
        "url": {"type": "url", "format": "postgres"},
    },
    "adafruit": {
        # https://io.adafruit.com/api/docs/#authentication
        "header": {"type": "re", "format": f"X-AIO-Key: {secret_format['adafruit']}"},
        "url": {
            "type": "re",
            "format": f"x-aio-key={secret_format['adafruit']}",
        },
        "env": {
            "type": "re",
            "format": fr"ADAFRUIT_IO_KEY\s*\=\s*{secret_format['adafruit']}",
        },
    },
    "discord": {
        "url": {
            "type": "re",
            "format": f"client_id={secret_format['discord']}",
        },
        "bot": {
            "type": "re",
            "format": f"Authorization: Bot {secret_format['discord']}",
        },
    },
    "linode": {
        "env": {
            "type": "re",
            "format": fr"LINODE_API_TOKEN\s*=\s*{secret_format['linode']}",
        },
        "yaml": {
            "type": "re",
            "format": fr"LINODE_API_TOKEN\s*:\s*\"?{secret_format['linode']}\"?",
        },
        "bearer": {
            "type": "re",
            "format": f"Authorization: Bearer {secret_format['linode']}",
        },
    },
    "password": {"password": {"type": "re", "format": r"password=(\w+)"}},
}
