"""Built-in output formatters."""

from newsroom.formatters.base import BaseFormatter
from newsroom.formatters.html_fmt import HTMLFormatter
from newsroom.formatters.json_fmt import JSONFormatter
from newsroom.formatters.markdown import MarkdownFormatter
from newsroom.formatters.plaintext import PlainTextFormatter

FORMATTER_REGISTRY: dict[str, type[BaseFormatter]] = {
    "markdown": MarkdownFormatter,
    "json": JSONFormatter,
    "html": HTMLFormatter,
    "plaintext": PlainTextFormatter,
}

__all__ = [
    "BaseFormatter",
    "MarkdownFormatter",
    "JSONFormatter",
    "HTMLFormatter",
    "PlainTextFormatter",
    "FORMATTER_REGISTRY",
]
