"""Google Drive source — reads documents from Drive as Articles."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from newsroom.models import Article
from newsroom.sources.base import BaseSource
from newsroom.utils import parse_date

logger = logging.getLogger(__name__)

# MIME types for Google Workspace files and their export targets
_GDOC_MIME = "application/vnd.google-apps.document"
_GSHEET_MIME = "application/vnd.google-apps.spreadsheet"

_FILE_TYPE_QUERIES: dict[str, str] = {
    "gdoc": f"mimeType='{_GDOC_MIME}'",
    "md": "mimeType='text/markdown'",
    "txt": "mimeType='text/plain'",
}


class GoogleDriveSource(BaseSource):
    """Fetch documents from Google Drive folders and convert to Articles.

    Config keys:
        credentials_path:  Path to OAuth client secrets JSON (default: credentials.json).
        token_path:        Path to stored token JSON (default: token.json).
        folders:           List of Drive folder IDs to scan.
        file_types:        Which file types to include (default: [gdoc, md, txt]).
        max_files:         Maximum number of files to fetch (default: 50).
    """

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.credentials_path: str = config.get("credentials_path", "credentials.json")
        self.token_path: str = config.get("token_path", "token.json")
        self.folders: list[str] = config.get("folders", [])
        self.file_types: list[str] = config.get("file_types", ["gdoc", "md", "txt"])
        self.max_files: int = config.get("max_files", 50)
        self.name: str = config.get("name", "gdrive")
        self._service = None

    async def fetch(self, topic: str) -> list[Article]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._fetch_sync)

    # -- private helpers -----------------------------------------------------

    def _ensure_service(self):
        """Lazily build the Drive API service."""
        if self._service is None:
            from newsroom.gdrive_auth import get_drive_service
            self._service = get_drive_service(self.credentials_path, self.token_path)
        return self._service

    def _fetch_sync(self) -> list[Article]:
        try:
            service = self._ensure_service()
        except ImportError as exc:
            logger.error("Google Drive source '%s': %s", self.name, exc)
            return []
        except FileNotFoundError as exc:
            logger.error("Google Drive source '%s': %s", self.name, exc)
            return []

        articles: list[Article] = []
        for folder_id in self.folders:
            files = self._list_folder(service, folder_id)
            for file_meta in files:
                article = self._read_file(service, file_meta)
                if article:
                    articles.append(article)
                if len(articles) >= self.max_files:
                    break
            if len(articles) >= self.max_files:
                break

        logger.info("Google Drive source '%s': loaded %d files.", self.name, len(articles))
        return articles

    def _list_folder(self, service, folder_id: str) -> list[dict]:
        """List files in a Drive folder matching the configured file types."""
        mime_clauses = []
        for ft in self.file_types:
            q = _FILE_TYPE_QUERIES.get(ft)
            if q:
                mime_clauses.append(q)

        if not mime_clauses:
            logger.warning("No valid file_types configured for gdrive source '%s'.", self.name)
            return []

        mime_filter = " or ".join(mime_clauses)
        query = f"'{folder_id}' in parents and ({mime_filter}) and trashed=false"

        results: list[dict] = []
        page_token = None
        while True:
            resp = service.files().list(
                q=query,
                fields="nextPageToken, files(id, name, mimeType, modifiedTime, webViewLink)",
                pageSize=min(100, self.max_files - len(results)),
                pageToken=page_token,
            ).execute()

            results.extend(resp.get("files", []))
            page_token = resp.get("nextPageToken")
            if not page_token or len(results) >= self.max_files:
                break

        return results

    def _read_file(self, service, file_meta: dict) -> Article | None:
        """Download file content and build an Article."""
        file_id = file_meta["id"]
        mime = file_meta.get("mimeType", "")

        try:
            if mime == _GDOC_MIME:
                # Export Google Doc as plain text
                content = (
                    service.files()
                    .export(fileId=file_id, mimeType="text/plain")
                    .execute()
                    .decode("utf-8", errors="replace")
                )
            else:
                # Download regular file content
                content = (
                    service.files()
                    .get_media(fileId=file_id)
                    .execute()
                    .decode("utf-8", errors="replace")
                )
        except Exception:
            logger.warning("Failed to read file '%s' (%s).", file_meta.get("name"), file_id,
                           exc_info=True)
            return None

        return Article(
            title=file_meta.get("name", "Untitled"),
            url=file_meta.get("webViewLink", ""),
            source_name=self.name,
            published_at=parse_date(file_meta.get("modifiedTime")),
            content=content.strip(),
        )
