"""A Rich highlighter to highlight secrets"""
import re

from rich.text import Text
from rich.highlighter import RegexHighlighter

USER = r"[-0-9a-zA-Z$_+!`(),.?/;&=%#]+"
PASSWORD = r"(?P<yellow>[-0-9a-zA-Z$_+!`(),.?/;:&=%#]+)"

userpass = fr"{USER}:{PASSWORD}@"

URL_SECRET_RE = fr"[a-zA-Z]+[\w.]*://{userpass}[-0-9a-zA-Z$_+!`(),.?/;:&=%#]*"
BEARER_SECRET_RE = r".*Bearer\s+(?P<yellow>\w+)"
BOT_SECRET_RE = r".*Bot\s+(?P<yellow>\w+)"
COLON_SECRET_RE = r"[\w.-]+\s*:\s*(?P<yellow>[\w.-]+)"
EQUALS_SECRET_RE = r"[\w.-]+\s*=\s*(?P<yellow>[\w.-]+)"


class SecretHighlighter(RegexHighlighter):
    """Secret highlighter class"""

    def highlight(self, text: Text):
        for regex in [
            URL_SECRET_RE,
            BEARER_SECRET_RE,
            BOT_SECRET_RE,
            COLON_SECRET_RE,
            EQUALS_SECRET_RE,
        ]:
            re_match = re.match(regex, str(text))
            if re_match is not None:
                text.highlight_regex(regex)
                return

        re_match = re.match(r"(?P<yellow>.+)", str(text))
        text.highlight_regex(r"(?P<yellow>.+)")
