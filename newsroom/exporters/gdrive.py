"""Google Drive exporter — uploads digest results to Drive."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any

from newsroom.exporters.base import BaseExporter
from newsroom.models import Digest

logger = logging.getLogger(__name__)

_FORMAT_MIME: dict[str, str] = {
    "markdown": "text/markdown",
    "html": "text/html",
    "plaintext": "text/plain",
    "json": "application/json",
}

_FORMAT_EXT: dict[str, str] = {
    "markdown": ".md",
    "html": ".html",
    "plaintext": ".txt",
    "json": ".json",
}


class GoogleDriveExporter(BaseExporter):
    """Upload digest results to Google Drive.

    Config keys:
        credentials_path:    Path to OAuth client secrets JSON (default: credentials.json).
        token_path:          Path to stored token JSON (default: token.json).
        folder_id:           Target Drive folder ID (required).
        upload_as:           "file" or "gdoc" (default: "file").
        file_format:         "markdown", "html", "plaintext", "json" (default: "markdown").
        filename_template:   Template with {topic} and {date} placeholders.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.credentials_path: str = config.get("credentials_path", "credentials.json")
        self.token_path: str = config.get("token_path", "token.json")
        self.folder_id: str = config["folder_id"]
        self.upload_as: str = config.get("upload_as", "file")
        self.file_format: str = config.get("file_format", "markdown")
        self.filename_template: str = config.get("filename_template", "{topic}_{date}")

    async def export(self, digest: Digest, formatted: str) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._export_sync, digest, formatted)

    # -- private helpers -----------------------------------------------------

    def _ensure_service(self):
        from newsroom.gdrive_auth import get_drive_service
        return get_drive_service(self.credentials_path, self.token_path)

    def _build_filename(self, digest: Digest) -> str:
        safe_topic = "".join(
            c if c.isalnum() or c in " -_" else "" for c in digest.topic
        ).strip().replace(" ", "-")
        date_str = datetime.now().strftime("%Y-%m-%d")
        name = self.filename_template.format(topic=safe_topic, date=date_str)
        ext = _FORMAT_EXT.get(self.file_format, ".md")
        return f"{name}{ext}"

    def _export_sync(self, digest: Digest, formatted: str) -> str:
        try:
            service = self._ensure_service()
        except ImportError as exc:
            logger.error("Google Drive exporter: %s", exc)
            return f"error: {exc}"
        except FileNotFoundError as exc:
            logger.error("Google Drive exporter: %s", exc)
            return f"error: {exc}"

        # Lazy import — only needed when actually uploading
        from googleapiclient.http import MediaInMemoryUpload

        filename = self._build_filename(digest)
        content_bytes = formatted.encode("utf-8")

        if self.upload_as == "gdoc":
            # Upload and convert to Google Doc
            file_metadata = {
                "name": filename,
                "parents": [self.folder_id],
                "mimeType": "application/vnd.google-apps.document",
            }
            media = MediaInMemoryUpload(
                content_bytes,
                mimetype=_FORMAT_MIME.get(self.file_format, "text/markdown"),
                resumable=False,
            )
        else:
            # Upload as regular file
            mime = _FORMAT_MIME.get(self.file_format, "text/markdown")
            file_metadata = {
                "name": filename,
                "parents": [self.folder_id],
            }
            media = MediaInMemoryUpload(
                content_bytes,
                mimetype=mime,
                resumable=False,
            )

        created = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink",
        ).execute()

        link = created.get("webViewLink", created.get("id", "unknown"))
        logger.info("Google Drive exporter: uploaded '%s' → %s", filename, link)
        return link
