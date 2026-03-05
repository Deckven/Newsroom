"""Shared Google Drive OAuth2 authentication module.

All google-* imports are lazy (inside functions) so the rest of the
framework works without those packages installed.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.file",
]


def _require_google_packages() -> None:
    """Raise a clear error when google packages are missing."""
    try:
        import google.auth  # noqa: F401
        import google_auth_oauthlib  # noqa: F401
        import googleapiclient  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            "Google Drive integration requires additional packages. "
            "Install them with:\n"
            "  pip install google-auth google-auth-oauthlib google-api-python-client"
        ) from exc


def get_drive_service(
    credentials_path: str = "credentials.json",
    token_path: str = "token.json",
):
    """Build and return an authorized Google Drive API service.

    On first run, opens a browser for the OAuth2 consent flow and
    saves the token for future use.
    """
    _require_google_packages()

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    token_file = Path(token_path)

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        logger.info("Refreshing expired Google Drive token.")
        creds.refresh(Request())
    elif not creds or not creds.valid:
        creds_file = Path(credentials_path)
        if not creds_file.exists():
            raise FileNotFoundError(
                f"Google OAuth credentials file not found: {creds_file}\n"
                "Download it from Google Cloud Console → APIs & Services → Credentials."
            )
        flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), SCOPES)
        creds = flow.run_local_server(port=0)
        logger.info("Google Drive OAuth2 flow completed successfully.")

    # Persist token for next run
    token_file.write_text(creds.to_json(), encoding="utf-8")

    return build("drive", "v3", credentials=creds)


def revoke_token(token_path: str = "token.json") -> bool:
    """Revoke the stored token and delete the file.

    Returns True if successfully revoked, False otherwise.
    """
    _require_google_packages()

    import requests
    from google.oauth2.credentials import Credentials

    token_file = Path(token_path)
    if not token_file.exists():
        logger.info("No token file found at %s — nothing to revoke.", token_path)
        return False

    creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    resp = requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": creds.token},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token_file.unlink()

    if resp.status_code == 200:
        logger.info("Google Drive token revoked and deleted.")
        return True

    logger.warning("Revoke request returned %d, but token file was deleted.", resp.status_code)
    return False


def token_status(token_path: str = "token.json") -> dict:
    """Return info about the stored token (for the CLI status command)."""
    token_file = Path(token_path)
    if not token_file.exists():
        return {"authenticated": False, "path": str(token_file)}

    try:
        data = json.loads(token_file.read_text(encoding="utf-8"))
        return {
            "authenticated": True,
            "path": str(token_file),
            "scopes": data.get("scopes", []),
            "client_id": data.get("client_id", "")[:20] + "...",
        }
    except Exception:
        return {"authenticated": False, "path": str(token_file), "error": "corrupt token file"}
