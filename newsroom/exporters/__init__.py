"""Built-in exporter plugins."""

from newsroom.exporters.base import BaseExporter
from newsroom.exporters.gdrive import GoogleDriveExporter
from newsroom.exporters.obsidian import ObsidianExporter

EXPORTER_REGISTRY: dict[str, type[BaseExporter]] = {
    "obsidian": ObsidianExporter,
    "gdrive": GoogleDriveExporter,
}

__all__ = [
    "BaseExporter",
    "ObsidianExporter",
    "GoogleDriveExporter",
    "EXPORTER_REGISTRY",
]
